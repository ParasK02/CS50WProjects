# Generated by Django 4.2.3 on 2023-08-12 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='category',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]