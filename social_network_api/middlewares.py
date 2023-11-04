from django.utils import timezone
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class UpdateLastRequestMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request) -> Response:
        try:
            # MARK: Use JWTAuthentication to check if the user is authenticated with JWT
            jwt_auth = JWTAuthentication().authenticate(request)
            if jwt_auth:
                user = jwt_auth[0]
                user.last_time_request = timezone.now()
                user.save()
        except InvalidToken:
            pass

        response = self.get_response(request)
        return response
