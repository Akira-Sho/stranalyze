# Generated by Django 2.2.5 on 2021-11-10 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0029_auto_20211110_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_url_name',
            field=models.CharField(default=False, max_length=30, verbose_name='ラケットurl表示名'),
        ),
    ]
