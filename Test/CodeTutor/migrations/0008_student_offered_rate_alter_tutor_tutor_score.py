# Generated by Django 5.0.6 on 2024-07-01 04:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CodeTutor', '0007_student_postal_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='offered_rate',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)]),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='tutor_score',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=4),
        ),
    ]