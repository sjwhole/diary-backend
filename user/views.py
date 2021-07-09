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
