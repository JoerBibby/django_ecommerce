# Generated by Django 3.2.5 on 2021-10-08 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_item_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='image_url',
        ),
        migrations.AddField(
            model_name='item',
            name='image_file',
            field=models.TextField(default='paceholder'),
        ),
    ]
