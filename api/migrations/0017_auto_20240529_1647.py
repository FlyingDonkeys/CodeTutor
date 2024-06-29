from django.db import migrations

def add_default_subjects(apps, schema_editor):
    Subject = apps.get_model('api', 'Subject')
    subjects = [
        ('H2_MATHEMATICS', 'H2 Mathematics'),
        ('H2_PHYSICS', 'H2 Physics'),
        ('H2_CHEMISTRY', 'H2 Chemistry'),
        ('H2_ECONOMICS', 'H2 Economics'),
    ]
    for code, name in subjects:
        Subject.objects.create(subject_name=code)

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_student_code_alter_student_date_joined_and_more'),  # Replace with the actual previous migration file
    ]

    operations = [
        migrations.RunPython(add_default_subjects),
    ]
