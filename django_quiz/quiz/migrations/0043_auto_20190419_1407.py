# Generated by Django 2.1.7 on 2019-04-19 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0042_quiz_anonymous'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='anonymous',
            field=models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='N', max_length=1),
        ),
    ]
