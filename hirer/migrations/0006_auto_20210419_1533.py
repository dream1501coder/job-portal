# Generated by Django 3.1.1 on 2021-04-19 15:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hirer', '0005_auto_20200422_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_bid_rate',
            name='create_at',
            field=models.DateTimeField(default=django.utils.timezone.localtime),
        ),
        migrations.AlterField(
            model_name='project_bid_rate',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.localtime),
        ),
    ]
