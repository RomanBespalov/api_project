from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator
from reviews.models import Category, Comment, Genre, Review, Title, User


'''Пользовательские сериализаторы (User)'''


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254
    )

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


class UserProfileSerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField()

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


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


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=6,
        required=True
    )


'''Категории. Жанры. Титлы. Ревью. Комменты.'''


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
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
        fields = ('id', 'text', 'author', 'pub_date')
