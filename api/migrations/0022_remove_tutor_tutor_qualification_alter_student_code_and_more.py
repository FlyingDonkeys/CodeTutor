# Generated by Django 5.0.6 on 2024-05-29 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_student_isstudent_tutor_isstudent_alter_student_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutor',
            name='tutor_qualification',
        ),
        migrations.AlterField(
            model_name='student',
            name='code',
            field=models.CharField(default='B43356', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='code',
            field=models.CharField(default='B43356', max_length=10, unique=True),
        ),
    ]
