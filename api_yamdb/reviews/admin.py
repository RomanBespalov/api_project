from django.contrib import admin
from reviews.models import User, Titles, Categories, Genres

admin.site.register(User)
admin.site.register(Titles)
admin.site.register(Categories)
admin.site.register(Genres)
