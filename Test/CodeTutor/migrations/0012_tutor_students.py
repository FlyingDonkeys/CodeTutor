# Generated by Django 5.0.6 on 2024-07-05 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CodeTutor', '0011_hiringapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='students',
            field=models.ManyToManyField(related_name='tutors', to='CodeTutor.student'),
        ),
    ]
