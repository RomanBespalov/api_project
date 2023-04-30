from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator

from reviews.models import Category, Comment, Genre, Review, Title, User


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
    username = serializers.CharField(
        max_length=150,
        validators=[MaxLengthValidator(150)]
    )
    first_name = serializers.CharField(
        max_length=150,
        validators=[MaxLengthValidator(150)]
    )
    last_name = serializers.CharField(
        max_length=150,
        validators=[MaxLengthValidator(150)]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=(MaxLengthValidator(254),),
    )

    class Meta:
        fields = '__all__'
        model = User


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenresSerializer(many=True, )
    category = CategoriesSerializer(many=False, required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',
                  'rating')
        model = Title


class CreateTitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        required=False,
        slug_field='slug',
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        many=False,
        required=False,
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    def create(self, validated_data):
        if Review.objects.filter(
            author=self.context['request'].user,
            title=validated_data.get('title')
        ).exists():
            raise serializers.ValidationError(
                'Нельзя оставить больше одного обзора.')

        review = Review.objects.create(**validated_data,)

        return review

    class Meta:
        model = Review
        exclude = ('title',)


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        exclude = ('review',)


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=6,
        required=True
    )


class UserProfileSerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField()

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User
