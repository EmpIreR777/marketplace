from django.db import migrations


def alter_age_category(apps, schema_editor):
    AgeCategory = apps.get_model('courses', 'AgeCategory')
    Course = apps.get_model('courses', 'Course')
    School = apps.get_model('courses', 'School')
    
    for_children = AgeCategory.objects.create(name='for_children', translations='Для детей')
    for_adults = AgeCategory.objects.create(name='for_adults', translations='Для взрослых')
    
    courses = Course.objects.all()
    
    school_ids = School.objects.values_list('course_ptr_id', flat=True)
    
    print("Всего курсов:", courses.count())
    print("Школ:", len(school_ids))
    
    for course in courses:
        try:
            if course.id in school_ids:
                course.age_category.add(for_children)
                print(f"Курсу {course.name} (школа) установлена категория 'Для детей'")
            else:
                course.age_category.add(for_adults)
                print(f"Курсу {course.name} установлена категория 'Для взрослых'")
        except Exception as e:
            print(f"Ошибка при обработке курса {course.id}: {e}")
            continue
    
    AgeCategory.objects.exclude(
        name__in=['for_children', 'for_adults']
    ).delete()
    print("Удалены все категории возраста кроме 'Для детей' и 'Для взрослых'")


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_download_school_pictures'),
    ]

    operations = [
        migrations.RunPython(alter_age_category, reverse_code=migrations.RunPython.noop)
    ]

