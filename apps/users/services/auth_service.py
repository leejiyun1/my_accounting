from rest_framework_simplejwt.tokens import RefreshToken


class AuthService:
    @staticmethod
    def get_tokens_for_user(user):
        """
        JWT 토큰을 생성하여 반환합니다.
        """

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return {
            'refresh': str(refresh),
            'access': str(access),
        }