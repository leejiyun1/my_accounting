from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import LoginSerializer
from ..services import AuthService

class LoginView(APIView):
    """
    사용자 로그인 뷰
    """

    def post(self, request, *args, **kwargs):
        # 요청 데이터 유효성 검사
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 사용자 인증 및 토큰 생성
        user = serializer.validated_data['user']
        token = AuthService.generate_token_for_user(user)

        # 응답 반환
        return Response({'token': token}, status=status.HTTP_200_OK)
