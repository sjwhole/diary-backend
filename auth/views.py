from django.db import IntegrityError
from rest_auth.registration.views import RegisterView
from rest_auth.views import LoginView
from rest_framework import status
from rest_framework.response import Response


class MyLoginView(LoginView):
    def get_response(self):
        serializer_class = self.get_response_serializer()

        data = {
            'user': self.user,
            'token': self.token
        }

        serializer = serializer_class(instance=data, context={'request': self.request})
        headers = {'Token': serializer.data.get('token')}
        content = {
            'message': '로그인에 성공했습니다.'
        }
        response = Response(content, headers=headers, status=status.HTTP_200_OK)

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
            headers = self.get_success_headers(serializer.data)
            headers['Token'] = self.get_response_data(user).get('token')
            content = {
                'message': '회원가입에 성공했습니다.'
            }
            return Response(content, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError as e:
            content = {
                'message': str(e)
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
