# Generated by Django 2.1.7 on 2019-03-23 15:42

from django.db import migrations
import quiz.models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0027_auto_20190323_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='start_date',
            field=quiz.models.UnixTimestampField(auto_created=True, null=True),
        ),
    ]