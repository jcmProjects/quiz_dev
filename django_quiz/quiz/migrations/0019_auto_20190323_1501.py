# Generated by Django 2.1.7 on 2019-03-23 15:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0018_auto_20190323_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]