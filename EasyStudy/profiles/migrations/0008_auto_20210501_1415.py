# Generated by Django 3.0.5 on 2021-05-01 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20210427_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, default='Profile.objects.get_current', to='profiles.Profile'),
        ),
    ]
