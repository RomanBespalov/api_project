from django.contrib import admin
from reviews.models import User, Title, Category, Genre, Review, Comment


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'role', 'bio', 'first_name', 'last_name'
    )


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class GenresAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'year',
                    'description',
                    'get_genre',
                    'category')

    def get_genre(self, obj):
        return ", ".join(obj.genre.values_list("genre", flat=True))

    get_genre.short_description = 'Жанры'


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'author', 'score', 'pub_date')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'review', 'author', 'pub_date')


admin.site.register(User, UserAdmin)
admin.site.register(Title, TitlesAdmin)
admin.site.register(Category, CategoriesAdmin)
admin.site.register(Genre, GenresAdmin)
admin.site.register(Review, ReviewsAdmin)
admin.site.register(Comment, CommentsAdmin)
