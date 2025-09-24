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

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        token = AuthService.generate_token_for_user(user)

        return Response({'token': token}, status=status.HTTP_200_OK)
