from django.contrib import admin
from reviews.models import User, Titles, Categories, Genres, Reviews, Comments


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'role', 'bio', 'first_name', 'last_name'
    )


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class GenresAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'description', 'get_genre', 'category')

    def get_genre(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])

    get_genre.short_description = 'Жанры'


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'author', 'score', 'pub_date')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'review', 'author', 'pub_date')


admin.site.register(User, UserAdmin)
admin.site.register(Titles, TitlesAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(Comments, CommentsAdmin)
