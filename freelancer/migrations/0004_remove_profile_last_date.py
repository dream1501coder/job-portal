# Generated by Django 3.2.2 on 2021-05-09 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0003_profile_last_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='last_date',
        ),
    ]