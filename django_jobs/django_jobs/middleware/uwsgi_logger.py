from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class UwsgiLoggingMiddleware(object):

    def process_request(self, request):
        """
        Adds a logvar, django_user, which contains the username of
        the user to uwsgi. The logvar can then be used to log the username
        for each request.
        """
        try:
            import uwsgi
            auth_tuple = JSONWebTokenAuthentication().authenticate(request)
            username = \
                auth_tuple[0].email if auth_tuple else getattr(
                    request.user, 'email', 'Anonymous'
                )
            uwsgi.set_logvar('django_user', username)
        except ImportError:
            pass
