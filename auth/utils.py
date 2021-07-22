from random import randint

from rest_framework_jwt.settings import api_settings

from user.models import User


def create_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token


def login_by_social(kakao_id):
    user = User.objects.get(kakao_id=kakao_id)
    return user


def register_by_social(kakao_id, nickname):
    while True:
        random_num = "".join([str(randint(0, 9)) for _ in range(4)])
        username = f"{nickname}#{random_num}"
        if not User.objects.filter(username=f"nickname#{random_num}").exists():
            break
    user = User.objects.create_user(username=username, kakao_id=kakao_id, nickname=nickname)

    return user
