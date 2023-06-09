# Generated by Django 4.2.1 on 2023-06-09 19:52

from django.db import migrations

def create_categories(apps, schema_editor):
    Category = apps.get_model('auctions', 'Category')
    Category.objects.create(name='Fashion')
    Category.objects.create(name='Toys')
    Category.objects.create(name='Electronics')
    Category.objects.create(name='Home')
    Category.objects.create(name='Sports')

class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_listing_comment_bid'),
    ]

    operations = [
        migrations.RunPython(create_categories),
    ]
