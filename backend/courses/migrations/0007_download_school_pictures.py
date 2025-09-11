import json
import os
import requests
from PIL import Image
from io import BytesIO
from django.conf import settings
from pathlib import Path
from django.db import migrations


def download_and_convert_png_to_webp(image_url: str, course_id: str, folder_name: str):
    try:
        media_path = os.path.join(settings.MEDIA_ROOT, folder_name, str(course_id))
        os.makedirs(media_path, exist_ok=True)
        img_name = os.path.splitext(os.path.basename(image_url))[0] + '.webp'
        img_path = os.path.join(media_path, img_name)
        
        if os.path.exists(img_path):
            print(f"Изображение для курса {course_id} уже загружено {img_name}")
            return f"{folder_name}/{course_id}/{img_name}"
            
        response = requests.get(image_url, timeout=60)
        if response.status_code != 200:
            raise Exception(f"Не удалось загрузить изображение. Статус код: {response.status_code}")
            
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            raise Exception(f"Некорректный content-type: {content_type}")
            
        if len(response.content) == 0:
            raise Exception("Файл пустой")
            
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGB")
        img.save(img_path, format="WEBP", quality=100)
        return f"{folder_name}/{course_id}/{img_name}"
    except Exception as e:
        print(f"Ошибка загрузки изображения ({image_url}): {e}")
        return None


def download_school_pictures(apps, schema_editor):
    School = apps.get_model('courses', 'School')
    Course = apps.get_model('courses', 'Course')
    CourseImage = apps.get_model('courses', 'CourseImage')
    
    base_path = Path(__file__).resolve().parent.parent.parent
    file_path = os.path.join(base_path, "maintenance", "files", "schools_data_clean.json")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        schools_data = {item["name"]: item for item in data["items"]}
        print("Данные из JSON:", schools_data.keys())
        
        schools = School.objects.all()
        print("Школы в базе:", [school.name for school in schools])
        
        for school in schools:
            try:
                course = Course.objects.get(id=school.course_ptr_id)
                print(f"Проверяем школу: {course.name}")
                
                school_data = schools_data.get(course.name)
                if not school_data:
                    print(f"Нет данных для школы с именем '{course.name}'")
                    continue
                
                print(f"Найдены данные для школы: {school_data['name']}")
                
                course.link = school_data["link"]
                course.save()
                print(f"Обновлена ссылка для курса: {course.link}")
                
                img_path = download_and_convert_png_to_webp(school_data["image"], course.id, "courses")
                if img_path:
                    CourseImage.objects.create(course=course, image=img_path)
                    print(f"Загружено изображение для школы {school.id}")
                
            except Course.DoesNotExist:
                print(f"Не найден курс для школы {school.id}")
                continue
            except Exception as e:
                print(f"Ошибка при обработке школы {school.id}: {e}")
                continue
                
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
    except json.JSONDecodeError:
        print("Ошибка при парсинге JSON файла")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0006_activated_schools'),
    ]

    operations = [
        migrations.RunPython(download_school_pictures, reverse_code=migrations.RunPython.noop)
    ]
