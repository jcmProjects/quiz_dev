# Generated by Django 2.1.7 on 2019-03-23 15:20

from django.db import migrations
import django.utils.timezone
import unixtimestampfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0021_auto_20190323_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='start_date',
            field=unixtimestampfield.fields.UnixTimeStampField(default=django.utils.timezone.now),
        ),
    ]
