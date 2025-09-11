

import os
import uuid


def create_many_to_many_fields_courses(course, items, model, m2m_field):
    """Создание связей многие ко многим для курсов"""
    instances = [
        model.objects.get_or_create(name=item if isinstance(item, str) else item.name)[0]
        for item in items
    ]
    getattr(course, m2m_field).add(*instances)


def get_many_to_many_values(queryset):
    """Получение значений связей многие ко многим"""
    return list(queryset.values_list('name', flat=True))


def get_path_upload_course_files(instance, file_name):
    base, ext = os.path.splitext(file_name)
    base = str(uuid.uuid4())
    filename = f"{base}{ext}"
    return f"courses/course_files/{instance.course.id}/{filename}"

def get_path_upload_course_image(instance, file_name):
    base, ext = os.path.splitext(file_name)
    base = str(uuid.uuid4())
    filename = f"{base}{ext}"
    return f"courses/courses_images/{instance.course.id}/{filename}"