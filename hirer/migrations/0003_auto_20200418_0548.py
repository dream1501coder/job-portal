# Generated by Django 3.0.3 on 2020-04-18 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hirer', '0002_auto_20200418_0241'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='email',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user_id',
        ),
        migrations.AddField(
            model_name='comment',
            name='fname',
            field=models.CharField(default='0', max_length=35),
        ),
        migrations.AddField(
            model_name='comment',
            name='lname',
            field=models.CharField(default='0', max_length=35),
        ),
        migrations.AddField(
            model_name='comment',
            name='message',
            field=models.CharField(default='0', max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='subject',
            field=models.CharField(default='0', max_length=35),
        ),
    ]