from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('vuz', '0005_load_initial_data'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='programs',
            index=models.Index(fields=['form'], name='programs_form_idx'),
        ),
        migrations.AddIndex(
            model_name='programs',
            index=models.Index(fields=['faculty'], name='programs_faculty_idx'),
        ),
        migrations.AddIndex(
            model_name='programs',
            index=models.Index(fields=['specialty'], name='programs_specialty_idx'),
        ),
    ] 