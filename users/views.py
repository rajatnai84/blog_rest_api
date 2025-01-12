from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import (LoginSerializer, UserRegisterSerializer,
                               UserSerializer)

User = get_user_model()

class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserListCreateView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [IsAdminUser]

class UserRetrieveUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(
            {"detail":"Your account is successfully deleted."},
            status=status.HTTP_204_NO_CONTENT
        )

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

