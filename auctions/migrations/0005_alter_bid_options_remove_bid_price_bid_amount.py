# Generated by Django 4.2.1 on 2023-06-12 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_user_watchlist'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bid',
            options={'ordering': ['-amount']},
        ),
        migrations.RemoveField(
            model_name='bid',
            name='price',
        ),
        migrations.AddField(
            model_name='bid',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
            preserve_default=False,
        ),
    ]