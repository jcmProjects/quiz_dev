# Generated by Django 2.1.7 on 2019-03-22 23:22

from django.db import migrations
import quiz.models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0014_auto_20190322_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='date_time',
            field=quiz.models.UnixTimestampField(auto_created=True, null=True),
        ),
    ]
