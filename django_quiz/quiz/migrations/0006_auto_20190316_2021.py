# Generated by Django 2.1.7 on 2019-03-16 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20190316_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='course',
            field=models.ManyToManyField(to='users.Course'),
        ),
    ]
