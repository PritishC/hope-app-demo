angular.module('jobsApp', ['ionic', 'ngStorage', 'ngResource', 'ngMessages',
                           //'com.2fdevs.videogular', 'com.2fdevs.videogular.plugins.controls',
                           //'info.vietnamcode.nampnq.videogular.plugins.youtube',
                           'youtube-embed', 'ngSanitize'])

.config(function ($stateProvider, $urlRouterProvider, $ionicConfigProvider) {
  // Don't show any text on back button.
  $ionicConfigProvider.backButton.previousTitleText(false).text('');

  $stateProvider
    .state('register', {
      url: "/register",
      templateUrl: "templates/register.html",
      controller: 'RegisterCtrl'
    })
    .state('login', {
      url: "/login",
      templateUrl: "templates/login.html",
      controller: 'LoginCtrl',
      params: {
        user: null
      },
      cache: false
    })
    .state('forgot-password', {
      url: "/forgot-password",
      templateUrl: "templates/forgot-password.html",
      controller: 'ForgotPasswordCtrl'
    })
    .state('menu', {
      url: "/menu",
      abstract: true,
      templateUrl: "templates/menu.html",
      controller: 'MenuCtrl',
      cache: false
    })
    .state('menu.tabs', {
      url: "/tab",
      views: {
        'menuContent' :{
          templateUrl: "templates/menu/tabs.html"
        }
      }
    })
    .state('menu.tabs.buttons', {
      url: "/buttons",
      views: {
        'job-tab': {
          templateUrl: "templates/menu/tabs/buttons.html",
          controller: 'JobListCtrl'
        }
      },
      cache: false
    })
    .state('menu.tabs.list', {
      url: "/list",
      views: {
        'uni-tab': {
          templateUrl: "templates/menu/tabs/list.html",
          controller: 'UniListCtrl'
        }
      },
      cache: false
    })
    .state('menu.tabs.jobitem', {
      url: "/jobitem",
      views: {
        'job-tab': {
          templateUrl: "templates/menu/tabs/item.html",
          controller: 'JobItemCtrl'
        }
      },
      params: {
        content: null
      },
      cache: false
    })
    .state('menu.tabs.listitem', {
      url: "/listitem",
      views: {
        'uni-tab': {
          templateUrl: "templates/menu/tabs/item.html",
          controller: 'ListItemCtrl'
        }
      },
      params: {
        content: null
      }
    })
    .state('menu.tabs.form', {
      url: "/form",
      views: {
        'form-tab': {
          templateUrl: "templates/menu/tabs/form.html"
        }
      }
    })
    .state('menu.keyboard', {
      url: "/keyboard",
      views: {
        'menuContent': {
          templateUrl: "templates/menu/keyboard.html"
        }
      }
    })
    .state('menu.slidebox', {
      url: "/slidebox",
      views: {
        'menuContent': {
          templateUrl: "templates/menu/slidebox.html",
          controller: 'SlideboxCtrl'
        }
      }
    })
    .state('menu.about', {
      url: "/about",
      views: {
        'menuContent': {
          templateUrl: "templates/menu/about.html"
        }
      }
    });

  $urlRouterProvider.otherwise("login");

})

.config(['$httpProvider', function($httpProvider) {
  $httpProvider.interceptors.push([
    '$localStorage',
    '$location',
    '$q',
    '$injector',
    function($localStorage, $location, $q, $sessionStorage, $injector) {
      return {
        'request': function(config) {
          // Intercepts requests to inject the token
          config.headers = config.headers || {};
          if($localStorage.token) {
            config.headers.Authorization = 'JWT ' + $localStorage.token;
          }
          return config;
        },
        'responseError': function (response) {
          // Use $injector to fetch the service - prevents circular dependency
          Auth = $injector.get('Auth');
          $state = $injector.get('$state');

          if (response.status === 401 || response.status === 403) {
            // Delete the token, clear in-session storage and browser cache
            Auth.logout(function() {
              $state.go('login', null, {location: 'replace'});
            });
          }
          return $q.reject(response);
        }
      }
    }
  ]);
}])

.config(['$resourceProvider', function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
}])

.config(['$ionicConfigProvider', function($ionicConfigProvider) {
  // No need for JS scrolling, use native.
  $ionicConfigProvider.scrolling.jsScrolling(false);
  // No need to apply platform specific styling for tabs.
  // Undocumented value "none", thanks a lot Ionic.
  $ionicConfigProvider.tabs.position("top");
  // Removes the white highlighting (striped) when a tab is selected.
  $ionicConfigProvider.tabs.style("standard");
}])

.constant('apiDomain', 'http://54.169.111.11/')
.constant('apiUrl', 'http://54.169.111.11/virmire-api/');
//.constant('apiDomain', 'http://192.168.1.8:8000/')
//.constant('apiUrl', 'http://192.168.1.8:8000/virmire-api/');
