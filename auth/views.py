import requests
from django.conf import settings
from django.contrib.auth.models import update_last_login
from django.db import IntegrityError
from rest_auth.registration.views import RegisterView
from rest_auth.views import LoginView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user.models import User
from .exceptions import SocialException
from .utils import create_token, login_by_social, register_by_social


class MyLoginView(LoginView):
    def get_response(self):
        serializer_class = self.get_response_serializer()

        data = {
            'user': self.user,
            'token': self.token
        }

        serializer = serializer_class(instance=data, context={'request': self.request})

        content = {
            'Token': serializer.data.get('token')
        }
        response = Response(content, status=status.HTTP_200_OK)

        from rest_framework_jwt.settings import api_settings as jwt_settings
        if jwt_settings.JWT_AUTH_COOKIE:
            from datetime import datetime
            expiration = (datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA)
            response.set_cookie(jwt_settings.JWT_AUTH_COOKIE, self.token, expires=expiration, httponly=True)

        return response


class MyRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.perform_create(serializer)

            content = {
                'Token': self.get_response_data(user).get('token')
            }
            return Response(content, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            content = {
                'message': str(e)
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def kakao(request):
    try:
        app_rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY', None)
        redirect_uri = getattr(settings, 'KAKAO_REDIRECT_URI', None)
        user_token = request.data.get("code")

        # post request
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_rest_api_key}&redirect_uri={redirect_uri}&code={user_token}"
        )
        token_response_json = token_request.json()
        error = token_response_json.get("error", None)

        # if there is an error from token_request
        if error is not None:
            raise SocialException()
        access_token = token_response_json.get("access_token")

        # post request
        profile_request = requests.post(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()

        # parsing profile json
        kakao_id = profile_json["id"]
        nickname = profile_json["kakao_account"]["profile"]["nickname"]
        try:
            user = login_by_social(kakao_id)
        except User.DoesNotExist:
            user = register_by_social(kakao_id, nickname)

        token = create_token(user)

        update_last_login(None, user)

        content = {
            "Token": token
        }
        return Response(content)
    except SocialException as e:
        content = {
            "message": str(e)
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        content = {
            "message": str(e)
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
