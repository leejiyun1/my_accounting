from rest_framework.views import APIView
from apps.users.serializers.signup import SignupSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

class SignUpView(APIView):
    """
    회원가입 API 뷰
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        # 회원가입 처리
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # 응답 반환
        return Response({
            "message": "회원가입이 완료되었습니다.",
            "user": {
                "id": user.id,
                "nickname": user.nickname,
                "email": user.email,
            },
            "token": {
                "access": str(access),
                "refresh": str(refresh),
            }
        }, status=status.HTTP_201_CREATED
        )

