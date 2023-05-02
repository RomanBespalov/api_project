import csv
from django.core.management.base import BaseCommand

from api_yamdb.api_yamdb.reviews.models import Comment


class Command(BaseCommand):
    help = 'Import data from csv file'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        filename = options['filename']
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                mymodel = Comment()
                mymodel.review_id = row['review_id']
                mymodel.text = row['text']
                mymodel.author_id = row['author']
                mymodel.pub_date = row['pub_date']
                mymodel.save()
