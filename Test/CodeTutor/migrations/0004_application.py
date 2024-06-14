# Generated by Django 5.0.6 on 2024-06-14 11:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CodeTutor', '0003_commonuser_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_date', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_applications', to='CodeTutor.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CodeTutor.subject')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_applications', to='CodeTutor.tutor')),
            ],
        ),
    ]
