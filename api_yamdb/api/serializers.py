from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Categories, Comments, Genres, Reviews, Titles
from django.contrib.auth import get_user_model
from reviews.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator

class TokenObtainPairSerializer(serializers.Serializer): #in view
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


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(
        max_length=150,
        required=True,
        validators=[UnicodeUsernameValidator()],
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if username == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не должно быть "me"'
            )

        if not User.objects.filter(
            username=username,
            email=email
        ).exists():
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError(
                    f'Имя {username} уже занято'
                )
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    f'Почта {email} уже занята'
                )
        return data

    class Meta:
        fields = (
            'username', 'email'
        )
        model = User


class UserSignUpSerializer(serializers.ModelSerializer): # in view

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


class UserSerializer(serializers.ModelSerializer): # in view
    email = serializers.EmailField(
        max_length=254
    )

    class Meta:
        fields = '__all__'
        model = User


class TitlesSerializer(serializers.ModelSerializer): # in view

    class Meta:
        fields = '__all__'
        model = Titles


class CategoriesSerializer(serializers.ModelSerializer): # in view

    class Meta:
        fields = '__all__'
        model = Categories


class GenresSerializer(serializers.ModelSerializer): # in view

    class Meta:
        fields = '__all__'
        model = Genres


class ReviewsSerializer(serializers.ModelSerializer): # in view
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    def create(self, validated_data):
        if Reviews.objects.filter(
            author=self.context['request'].user,
            title=validated_data.get('title')
        ).exists():
            raise serializers.ValidationError(
                'Нельзя оставить больше одного обзора.')

        review = Reviews.objects.create(**validated_data,)

        return review

    class Meta:
        model = Reviews
        exclude = ('title',)


class CommentsSerializer(serializers.ModelSerializer): # in view
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comments
        exclude = ('review',)
