
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework import status

from config.util.response_handler.custom_response_handler import custom_response_handler
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from .serializers import AuthTokenObtainPairSerializer, AuthTokenRefreshSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = AuthTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            token_data = serializer.validated_data
                        
            # Use custom_response_handler to return the response
            return custom_response_handler(
                data=token_data, 
                status=status.HTTP_200_OK,
                message="Authenticated successfully"
            )
        except AuthenticationFailed as e:
            return Response({"error": "No active account found with the given credentials"}, status=status.HTTP_401_UNAUTHORIZED)
  
        
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = AuthTokenRefreshSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_data = serializer.validated_data
        
        return custom_response_handler(
            data=token_data, 
            status=status.HTTP_200_OK,
            message="Token refreshed successfully"
        )