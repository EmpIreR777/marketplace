from django.db import migrations


def activate_all_users(apps, schema_editor):
    CustomUser = apps.get_model('userauth', 'CustomUser')
    CustomUser.objects.all().update(is_active=True)


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0002_customuser_created_at_customuser_updated_at'),
    ]

    operations = [
        migrations.RunPython(activate_all_users, reverse_code=migrations.RunPython.noop)
    ]
