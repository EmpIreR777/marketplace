from django.db import migrations, models


def activate_all_schools(apps, schema_editor):
    School = apps.get_model('courses', 'School')
    School.objects.all().update(is_active=True, is_moderated=True)


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_thematicstype_learning_type'),
    ]

    operations = [
        migrations.RunPython(activate_all_schools, reverse_code=migrations.RunPython.noop)
    ]

