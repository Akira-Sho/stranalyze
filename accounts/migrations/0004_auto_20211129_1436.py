# Generated by Django 2.2.5 on 2021-11-29 05:36

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20211129_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(error_messages={'required': 'この項目は入力必須です。', 'unique': 'この名前はすでに使用されています。'}, max_length=15, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='username'),
        ),
    ]
