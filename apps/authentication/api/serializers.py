
from typing import Any, Dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from apps.users.api.serializers import UserDetailsSerializer


class AuthTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(AuthTokenObtainPairSerializer, self).validate(attrs)
        user_serializer = UserDetailsSerializer(self.user)
        data.update({'user_info': user_serializer.data}) # type: ignore
        return data
    
    
class AuthTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        return super().validate(attrs)