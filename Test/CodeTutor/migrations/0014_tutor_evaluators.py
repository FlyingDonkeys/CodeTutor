# Generated by Django 5.0.6 on 2024-07-07 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CodeTutor', '0013_alter_hiringapplication_offered_rates'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='evaluators',
            field=models.ManyToManyField(related_name='evaluated_tutors', to='CodeTutor.student'),
        ),
    ]
