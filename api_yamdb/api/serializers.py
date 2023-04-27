from rest_framework import serializers

from reviews.models import Categories, Comments, Genres, Reviews, Titles


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


class ReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Reviews


class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Comments
