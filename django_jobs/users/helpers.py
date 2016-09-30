from users.serializers import UserSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Custom implementation to return additional data alongwith
    the token.
    """
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data,
    }
