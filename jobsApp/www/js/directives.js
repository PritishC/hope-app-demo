angular.module('jobsApp')

/* Adds the ui-sref link for videos/articles */
.directive('checkPremium', [
  '$compile',
  '$localStorage',
  function($compile, $localStorage) {
    return {
      restrict: 'A',
      link: function(scope, element, attrs) {
        user = $localStorage.user;

        if(attrs.isPremium === "false" ||
           (attrs.isPremium === "true" && user.subscribed)) {
          element.attr('ui-sref', "menu.tabs.jobitem({content: item})");
          // Remove the attribute before compiling so that infinite
          // compilation does not occur.
          element.removeAttr('is-premium');
          $compile(element)(scope);
        }
      }
    }
  }
])

/* Hide tabs in a particular view */
.directive('hideTabs', [
  '$rootScope',
  function($rootScope) {
    return {
        restrict: 'A',
        link: function($scope, $el, attributes) {
            $scope.$watch(attributes.hideTabs, function(value){
              if(attributes.hideTabs === "true") {
                $rootScope.hideTabs = true;
              }
            });

            $scope.$on('$ionicView.beforeLeave', function() {
                $rootScope.hideTabs = false;
            });
        }
    };
  }
]);
