from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class LogoutView(APIView):
    """
    View to handle user logout.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 토큰 블랙리스트
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

        # 응답 반환
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
