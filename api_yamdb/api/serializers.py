from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Titles, Categories, Genres
from django.contrib.auth import get_user_model


class TokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, attrs):
        user = get_object_or_404(
            get_user_model(), username=attrs.get('username')
        )
        if user.confirmation_code != attrs.get('confirmation_code'):
            raise serializers.ValidationError(
                'Некорректный код подтверждения'
            )
        refresh = RefreshToken.for_user(user)
        data = {'access_token': str(refresh.access_token)}
        return data


class UserSignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username')

    def validate(self, attrs):
        super().validate(attrs)
        if attrs.get('username') == 'me':
            raise serializers.ValidationError(
                'Некорректное имя пользователя'
            )
        return attrs


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Titles


class TitlesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Titles


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Categories


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genres
