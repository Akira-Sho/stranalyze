# Generated by Django 2.2.5 on 2021-10-11 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0020_auto_20211011_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='display',
            field=models.BooleanField(default=False, verbose_name='表示'),
        ),
    ]
