# Generated by Django 3.0.5 on 2021-04-25 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0011_auto_20210425_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='category',
        ),
        migrations.AddField(
            model_name='file',
            name='categories',
            field=models.ManyToManyField(default=None, null=True, to='documents.Category'),
        ),
    ]
