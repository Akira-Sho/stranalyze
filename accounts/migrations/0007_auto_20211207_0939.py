# Generated by Django 2.2.5 on 2021-12-07 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20211129_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(error_messages={'unique': 'この名前はすでに使用されています。'}, max_length=15, unique=True, verbose_name='username'),
        ),
    ]
