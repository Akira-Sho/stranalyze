# Generated by Django 2.2.5 on 2021-06-28 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0009_auto_20210628_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(max_length=500, verbose_name='本文'),
        ),
    ]
