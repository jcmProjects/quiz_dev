# Generated by Django 2.1.7 on 2019-05-14 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20190502_1615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='valid_ans',
        ),
    ]