from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login

from rest_framework import viewsets, parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.compat import get_request_data

from users.serializers import UserSerializer, AuthCustomTokenSerializer
from users.permissions import IsAnonCreate

AppUser = get_user_model()
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint allowing users to be viewed or edited
    """
    queryset = AppUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (IsAnonCreate,)


class JSONWebToken(ObtainJSONWebToken):
    """
    Subclass for custom functionality.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=get_request_data(request)
        )

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)

            # Update last login
            update_last_login(None, user)

            return Response(response_data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainAuthToken(APIView):
    """
    Override to use custom token serializer
    NOTE: Not used in favour of JWT
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )

    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        content = {
            'token': unicode(token.key),
        }

        return Response(content)
