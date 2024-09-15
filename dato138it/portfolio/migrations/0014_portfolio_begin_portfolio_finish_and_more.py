# Generated by Django 5.0.2 on 2024-08-10 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0013_portfolio_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='begin',
            field=models.DateField(blank=True, null=True, verbose_name='Начало работы'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='finish',
            field=models.DateField(blank=True, null=True, verbose_name='Конец работы'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='specialization',
            field=models.CharField(default='test2', max_length=255, verbose_name='Специальность'),
            preserve_default=False,
        ),
    ]