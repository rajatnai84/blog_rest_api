from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'username',
            'name',
            'bio',
            'profile_picture',
            'phone_number',
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            name=validated_data.get('name'),
            bio=validated_data.get('bio'),
            phone_number=validated_data.get('phone_number'),
            profile_picture=validated_data.get('profile_picture'),
            password=validated_data['password'],
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(username=email, password=password)

        if user and user.check_password(password):
            tokens = RefreshToken.for_user(user)

            return {
                'refresh': str(tokens),
                'access': str(tokens.access_token),
                'user_id': user.id,
            }
        raise ValidationError({"detail": "Invalid credentials."})

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'name',
            'bio',
            'profile_picture',
            'phone_number',
        )
