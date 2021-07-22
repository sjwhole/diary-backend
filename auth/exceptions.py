class SocialException(Exception):
    def __str__(self):
        return "소셜 로그인 중 오류가 발생했습니다."
