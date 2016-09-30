angular.module('jobsApp')

.controller('RegisterCtrl', [
  '$scope',
  '$state',
  '$ionicPopup',
  'Auth',
  'utilityService',
  function($scope, $state, $ionicPopup, Auth, utilityService) {
    $scope.user = {};

    if(Auth.isLoggedIn()) {
      $state.go('menu.tabs.buttons', null, {location: 'replace'});
    }

    $scope.register = function(form) {
      if(!form.$valid) {
        return;
      }

      $scope.spinner = true;
      Auth.register($scope.user)
        .then(function(response) {
          $state.go('login', {user: $scope.user});
        }, function(response) {
          error = utilityService.errorMsgFromResponse(response);
          $ionicPopup.alert({
            title: 'Error',
            template: error
          })
          .then(function() {
            form.$submitted = false;
          });
        })
        .finally(function() {
          $scope.spinner = false;
        });
    };
  }
])

.controller('LoginCtrl', [
  '$scope',
  '$state',
  '$localStorage',
  '$ionicPopup',
  '$stateParams',
  'Auth',
  'utilityService',
  function($scope, $state, $localStorage, $ionicPopup, $stateParams,
           Auth, utilityService) {
    $scope.user = {};

    var moveForward = function() {
      $state.go('menu.tabs.buttons', null, {location: 'replace'});
    };

    var successCallback = function(response) {
      $localStorage.token = response.data.token;
      $localStorage.user = response.data.user;

      moveForward();
    };

    var errorCallback = function(response) {
      error = utilityService.errorMsgFromResponse(response);
      return $ionicPopup.alert({
        title: 'Error',
        template: error
      });
    };

    if(Auth.isLoggedIn()) {
      moveForward();
    }

    if($stateParams.user) {
      $scope.spinner = true;
      Auth.login($stateParams.user)
        .then(successCallback, errorCallback)
        .finally(function() {
          $scope.spinner = false;
        });
    }

    $scope.login = function(form) {
      if(!form.$valid) {
        return;
      }

      $scope.spinner = true;
      Auth.login($scope.user)
        .then(successCallback,
        function(response) {
          errorCallback(response)
            .then(function() {
              form.$submitted = false;
            });
        })
        .finally(function() {
          $scope.spinner = false;
        });
    };
  }
])

.controller('ForgotPasswordCtrl', [
  '$scope',
  '$state',
  'Auth',
  function($scope, $state, Auth) {
    if(Auth.isLoggedIn()) {
      $state.go('menu.tabs.buttons');
    }

    // TODO: Everything?
  }
])

.controller('UniListCtrl', [
  '$scope',
  '$state',
  '$ionicPopup',
  '$localStorage',
  '$sessionStorage',
  '$q',
  'Auth',
  'University',
  'utilityService',
  function ($scope, $state, $ionicPopup, $localStorage, $sessionStorage,
            $q, Auth, University, utilityService) {
    $scope.spinner = true;

    if(!$sessionStorage.universities) {
      $sessionStorage.universities = [];
    }

    // Fetch the refresh token everytime the user is on
    // the app.
    Auth.refresh()
      .then(function(response) {
        $localStorage.token = response.data.token;
        $localStorage.user = response.data.user;

        if($sessionStorage.universities.length) {
          return $q.resolve({
            results: $sessionStorage.universities
          });
        } else {
          return University.get().$promise;
        }
      }, function(response) {
        return $q.reject(response);
      })
      .then(function(response) {
        $scope.universities = response.results;
        $sessionStorage.universities = response.results;
        return $q.resolve(response);
      }, function(response){
        error = utilityService.errorMsgFromResponse(response);
        $ionicPopup.alert({
          title: 'Error',
          template: error
        }).then(function() {
          Auth.logout(function() {
            $state.go('login', null, {location: 'replace'});
          });
        });

        return $q.reject(response);
      })
      .finally(function() {
        $scope.spinner = false;
      });
  }
])

.controller('JobListCtrl', [
  '$scope',
  '$ionicPopup',
  '$ionicActionSheet',
  '$ionicModal',
  '$state',
  '$localStorage',
  '$sessionStorage',
  '$q',
  'Auth',
  'Article',
  'Video',
  'utilityService',
  function ($scope, $ionicPopup, $ionicActionSheet, $ionicModal, $state,
            $localStorage, $sessionStorage, $q, Auth, Article, Video,
            utilityService) {
    // Avoid flash of placeholder content
    $scope.objectsByCategory = {};
    $scope.spinner = true;
    $scope.user = $localStorage.user;

    if(!$sessionStorage.videos) {
      $sessionStorage.videos = [];
    }
    if(!$sessionStorage.articles) {
      $sessionStorage.articles = [];
    }

    var getVideos = function() {
      return Video.get().$promise;
    };

    var getArticles = function() {
      return Article.get().$promise;
    };

    var groupObjects = function() {
      var combined = $scope.videos.concat($scope.articles);
      angular.forEach(combined, function(object) {
        if(!(object.category in $scope.objectsByCategory)) {
          $scope.objectsByCategory[object.category] = [];
        }
        $scope.objectsByCategory[object.category].push(object);
      });
    };

    // Fetch the refresh token everytime the user is on
    // the app.
    Auth.refresh()
      .then(function(response) {
        $localStorage.token = response.data.token;
        $localStorage.user = response.data.user;

        if($sessionStorage.videos.length) {
          return $q.resolve({
            results: $sessionStorage.videos
          });
        } else {
          return getVideos();
        }
      }, function(response) {
        return $q.reject(response);
      })
      .then(function(response) {
        $scope.videos = response.results;
        $sessionStorage.videos = response.results;

        if($sessionStorage.articles.length) {
          return $q.resolve({
            results: $sessionStorage.articles
          });
        } else {
          return getArticles();
        }
      }, function(response) {
        return $q.reject(response);
      })
      .then(function(response) {
        $scope.articles = response.results;
        $sessionStorage.articles = response.results;

        groupObjects();
        return $q.resolve(response);
      }, function(response) {
        error = utilityService.errorMsgFromResponse(response);
        $ionicPopup.alert({
          title: 'Error',
          template: error
        }).then(function() {
          Auth.logout(function() {
            $state.go('login', null, {location: 'replace'});
          });
        });

        return $q.reject(response);
      })
      .finally(function() {
        $scope.spinner = false;
      });
  }
])

.controller('JobItemCtrl', [
  '$scope',
  '$stateParams',
  '$sce',
  '$localStorage',
  'Auth',
  function($scope, $stateParams, $sce, $localStorage, Auth) {
    $scope.content = $stateParams.content;
    $scope.user = $localStorage.user;

    // Assuming content is a video object
    $scope.config = {
      sources: [
        {src: "https://www.youtube.com/watch?v=0vrdgDdPApQ"}
      ],
      tracks: [],
      theme: "lib/videogular-themes-default/videogular.css",
      preload: "none",
      plugins: {
        controls: {
          autoHide: true,
          autoHideTime: 5000
        }
      }
    };

    $scope.trustAsHtml = $sce.trustAsHtml;
  }
])

.controller('ListItemCtrl', [
  '$scope',
  '$stateParams',
  '$sce',
  '$localStorage',
  'Auth',
  function($scope, $stateParams, $sce, $localStorage, Auth) {
    $scope.university = $stateParams.content;
    $scope.user = $localStorage.user;
    $scope.trustAsHtml = $sce.trustAsHtml;
  }
])

.controller('SlideboxCtrl', function($scope, $ionicSlideBoxDelegate) {
  $scope.nextSlide = function() {
    $ionicSlideBoxDelegate.next();
  }             
})              

.controller('MenuCtrl', [
  '$scope',
  '$ionicSideMenuDelegate',
  '$ionicModal',
  '$state',
  'Auth',
  function($scope, $ionicSideMenuDelegate, $ionicModal, $state, Auth) {
    $ionicModal.fromTemplateUrl('templates/modals/modal.html', function (modal) {
      $scope.modal = modal;
    }, {
      animation: 'slide-in-up'
    });

    $scope.logout = function() {
      Auth.logout(function() {
        $state.go('login', null, {location: 'replace'});
      });
    };
 }])
  
 .controller('AppCtrl', [
  function() {
    // Empty
}]);
