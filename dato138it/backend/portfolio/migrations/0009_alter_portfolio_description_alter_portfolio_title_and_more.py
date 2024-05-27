# Generated by Django 5.0.2 on 2024-04-03 13:03

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0008_alter_place_years'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Статья'),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='title',
            field=models.TextField(verbose_name='Достижение'),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
