# Generated by Django 3.2.2 on 2021-05-09 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin1', '0002_delete_payment_report'),
        ('freelancer', '0002_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_date',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='admin1.add_project'),
        ),
    ]
