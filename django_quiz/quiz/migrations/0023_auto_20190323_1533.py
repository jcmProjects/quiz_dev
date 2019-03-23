# Generated by Django 2.1.7 on 2019-03-23 15:33

from django.db import migrations
import django.utils.timezone
import unixtimestampfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0022_auto_20190323_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='date_time',
            field=unixtimestampfield.fields.UnixTimeStampField(default=django.utils.timezone.now),
        ),
    ]
