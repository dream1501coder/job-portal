# Generated by Django 3.2.2 on 2021-05-13 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hirer', '0010_alter_project_bid_rate_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_bid_rate',
            name='end_date',
            field=models.DateTimeField(),
        ),
    ]
