# Generated by Django 3.0.3 on 2020-04-18 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hirer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='firstname',
        ),
        migrations.AddField(
            model_name='comment',
            name='create_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='comment',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='project_bid_rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.IntegerField(default='0')),
                ('bid_rate', models.IntegerField(default='0')),
                ('comments', models.CharField(default='', max_length=500)),
                ('status', models.CharField(default='', max_length=50)),
                ('progress', models.CharField(default='', max_length=50)),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
