# Generated by Django 2.0.5 on 2018-05-24 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0007_auto_20180524_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='title',
            field=models.CharField(default='title', max_length=50),
        ),
    ]