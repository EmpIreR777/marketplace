from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('vuz', '0006_add_indexes'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='forms',
            index=models.Index(fields=['name'], name='forms_name_idx'),
        ),
    ] 