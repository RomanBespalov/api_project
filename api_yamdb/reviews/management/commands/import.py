import csv
from django.core.management.base import BaseCommand
from reviews.models import User, Titles, Categories, Genres, Reviews, Comments


# class Command(BaseCommand):
#     help = 'Import data from csv file'

#     def add_arguments(self, parser):
#         parser.add_argument('filename', type=str)

#     def handle(self, *args, **options):
#         filename = options['filename']
#         with open(filename, 'r') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 mymodel = User()
#                 mymodel.id = row['id']
#                 mymodel.username = row['username']
#                 mymodel.email = row['email']
#                 mymodel.role = row['role']
#                 mymodel.save()


# class Command(BaseCommand):
#     help = 'Import data from csv file'

#     def add_arguments(self, parser):
#         parser.add_argument('filename', type=str)

#     def handle(self, *args, **options):
#         filename = options['filename']
#         with open(filename, 'r') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 mymodel = Categories()
#                 mymodel.name = row['name']
#                 mymodel.slug = row['slug']
#                 mymodel.save()


# class Command(BaseCommand):
#     help = 'Import data from csv file'

#     def add_arguments(self, parser):
#         parser.add_argument('filename', type=str)

#     def handle(self, *args, **options):
#         filename = options['filename']
#         with open(filename, 'r') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 mymodel = Genres()
#                 mymodel.name = row['name']
#                 mymodel.slug = row['slug']
#                 mymodel.save()


# class Command(BaseCommand):
#     help = 'Import data from csv file'

#     def add_arguments(self, parser):
#         parser.add_argument('filename', type=str)

#     def handle(self, *args, **options):
#         filename = options['filename']
#         with open(filename, 'r') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 mymodel = Titles()
#                 mymodel.name = row['name']
#                 mymodel.year = row['year']
#                 mymodel.category_id = row['category']
#                 mymodel.save()


# class Command(BaseCommand):
#     help = 'Import data from csv file'

#     def add_arguments(self, parser):
#         parser.add_argument('filename', type=str)

#     def handle(self, *args, **options):
#         filename = options['filename']
#         with open(filename, 'r') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 title_obj = Titles.objects.get(id=row['title_id'])
#                 genre = Genres.objects.get(id=row['genre_id'])
#                 title_obj.genre.add(genre)


# class Command(BaseCommand):
#     help = 'Import data from csv file'

#     def add_arguments(self, parser):
#         parser.add_argument('filename', type=str)

#     def handle(self, *args, **options):
#         filename = options['filename']
#         with open(filename, 'r') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 mymodel = Reviews()
#                 mymodel.title_id = row['title_id']
#                 mymodel.text = row['text']
#                 mymodel.author_id = row['author']
#                 mymodel.score = row['score']
#                 mymodel.pub_date = row['pub_date']
#                 mymodel.save()


class Command(BaseCommand):
    help = 'Import data from csv file'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        filename = options['filename']
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                mymodel = Comments()
                mymodel.review_id = row['review_id']
                mymodel.text = row['text']
                mymodel.author_id = row['author']
                mymodel.pub_date = row['pub_date']
                mymodel.save()
