from rest_framework import serializers
from reviews.models import Categories, Comments, Genres, Reviews, Titles, User
from django.contrib.auth.validators import UnicodeUsernameValidator



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


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254
    )

    class Meta:
        fields = '__all__'
        model = User


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Categories


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenresSerializer(many=True, )
    category = CategoriesSerializer(many=False, required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',
                  'rating')
        model = Titles


class CreateTitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        required=False,
        slug_field='slug',
        queryset=Genres.objects.all(),
    )
    category = serializers.SlugRelatedField(
        many=False,
        required=False,
        slug_field='slug',
        queryset=Categories.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Titles


class ReviewsSerializer(serializers.ModelSerializer):
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


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    class Meta:
        model = Comments
        exclude = ('review',)


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    class Meta:
        fields = '__all__'
        model = Reviews


class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Comments


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
