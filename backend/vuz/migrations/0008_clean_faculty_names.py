from django.db import migrations
import re


def clean_faculty_names(apps, schema_editor):
    Faculty = apps.get_model('vuz', 'Faculties')
    pattern = r'^\d{2}\.\d{2}\.\d{2}\s+'
    
    print("\n=== НАЧАЛО ОЧИСТКИ НАЗВАНИЙ ФАКУЛЬТЕТОВ ===")
    
    faculties = Faculty.objects.all()
    updated_count = 0
    
    for faculty in faculties:
        if faculty.name:
            new_name = re.sub(pattern, '', faculty.name)
            if new_name != faculty.name:
                print(f"Изменение названия факультета: '{faculty.name}' -> '{new_name}'")
                faculty.name = new_name
                faculty.save()
                updated_count += 1
    
    print(f"\nОбновлено записей: {updated_count}")
    print("=== ОЧИСТКА НАЗВАНИЙ ФАКУЛЬТЕТОВ ЗАВЕРШЕНА ===\n")


def reverse_clean_faculty_names(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('vuz', '0007_add_forms_index'),
    ]

    operations = [
        migrations.RunPython(clean_faculty_names, reverse_clean_faculty_names),
    ] 