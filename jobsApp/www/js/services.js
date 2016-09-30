angular.module('jobsApp')

.factory('Auth', [
  '$http',
  '$localStorage',
  '$sessionStorage',
  'apiUrl',
  'apiDomain',
  function($http, $localStorage, $sessionStorage, apiUrl, apiDomain) {
    var Auth = this;

    function urlBase64Decode(str) {
       var output = str.replace('-', '+').replace('_', '/');
       switch (output.length % 4) {
           case 0:
               break;
           case 2:
               output += '==';
               break;
           case 3:
               output += '=';
               break;
           default:
               throw 'Illegal base64url string!';
       }
       return window.atob(output);
    }

    function getClaimsFromToken() {
      var token = $localStorage.token;
      var user = {};

      if(typeof token !== 'undefined') {
        var encoded = token.split('.')[1];
        user = JSON.parse(urlBase64Decode(encoded));
      }

      return user;
    }

    var tokenClaims = getClaimsFromToken();

    Auth.login = function(data) {
      // Gets the token
      return $http({
        method: 'POST',
        url: apiDomain + 'virmire-api-token-auth/', 
        data: data
      });
    };

    Auth.register = function(data) {
      return $http({
          method: 'POST',
          url: apiUrl + 'users/',
          data: data
      });
    };

    Auth.logout = function(successCallback) {
      tokenClaims = {};
      delete $localStorage.token;
      $sessionStorage.$reset();

      successCallback();
    };

    Auth.isLoggedIn = function() {
      return (typeof $localStorage.token !== 'undefined');
    };

    Auth.getTokenClaims = function() {
      return tokenClaims;
    };

    Auth.refresh = function() {
      return $http({
        method: 'POST',
        url: apiDomain + 'virmire-api-token-refresh/',
        data: {
          token: $localStorage.token
        }
      });
    };

    return Auth;
  }
])

.factory('Video', [
  '$resource',
  'apiUrl',
  function($resource, apiUrl) {
    var url = apiUrl + "videos/:id/",
        Video = $resource(url, {id: "@id"}, {});

    return Video;
  }
])

.factory('Article', [
  '$resource',
  'apiUrl',
  function($resource, apiUrl) {
    var url = apiUrl + "articles/:id/",
        Article = $resource(url, {id: "@id"}, {});

    return Article;
  }
])

.factory('University', [
  '$resource',
  'apiUrl',
  function($resource, apiUrl) {
    var url = apiUrl + "universities/:id/",
        University = $resource(url, {id: "@id"}, {});

    return University;
  }
])

.factory('utilityService', [
  function() {
    var utilityService = this;

    utilityService.errorMsgFromResponse = function(response) {
      responseMsg = '';

      if(response.status === 0) {
        responseMsg = 'Your internet is unstable or down, or the server is not reachable.'
      } else if(response.data) {
        if(response.data.hasOwnProperty('non_field_errors')) {
          for(var i = 0; i < response.data.non_field_errors.length; i++) {
            responseMsg += ('* ' + response.data.non_field_errors[i] + '\n');
          }
        } else {
          for(var key in response.data) {
            if(response.data.hasOwnProperty(key)) {
              responseMsg += ('* <strong>' + key + '</strong>: ' + response.data[key] + '\n');
            }
          }
        }
      }

      return responseMsg;
    };

    return utilityService;
  }
]);
