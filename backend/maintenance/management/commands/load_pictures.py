from django.core.management.base import BaseCommand
import json
from courses.models import Course
import os
import requests
from PIL import Image
from io import BytesIO
from core import settings
from pathlib import Path
from courses.models import CourseImage
from organizations.models import Organization
from urllib.parse import urlparse, unquote


class Command(BaseCommand):
    help = 'Project start'

    def handle(self, *args, **kwargs):
        self.check_courses_for_images()
        self.check_schools_for_images()
        self.load_logo_for_organizations()

    @staticmethod
    def _download_svg(image_url: str, obj, folder_name: str):
        try:
            media_path = os.path.join(settings.MEDIA_ROOT, folder_name, str(obj.id))
            os.makedirs(media_path, exist_ok=True)

            parsed_url = urlparse(image_url)
            img_name = os.path.basename(parsed_url.path)
            img_name = unquote(img_name)

            if ".svg" in img_name:
                img_name = img_name.split(".svg", 1)[0] + ".svg"
            else:
                raise Exception(f"Некорректное расширение файла: {img_name}")

            img_path = os.path.join(media_path, img_name)

            if os.path.exists(img_path):
                print(f"SVG {obj} уже загружен {img_name}")
                return f"{folder_name}/{obj.id}/{img_name}"

            response = requests.get(image_url, timeout=60)
            if response.status_code != 200:
                raise Exception(f"Не удалось загрузить изображение. Статус код: {response.status_code}")

            content_type = response.headers.get('Content-Type', '')
            if content_type != "image/svg+xml":
                raise Exception(f"Некорректный content-type: {content_type}")

            if len(response.content) == 0:
                raise Exception("Файл пустой")

            with open(img_path, "wb") as f:
                f.write(response.content)

            return f"{folder_name}/{obj.id}/{img_name}"

        except Exception as e:
            print(f"Ошибка загрузки SVG ({image_url}): {e}")
            return None

    @staticmethod
    def _download_and_convert_png_to_webp(image_url: str, obj, folder_name: str):
        try:
            media_path = os.path.join(settings.MEDIA_ROOT, folder_name, str(obj.id))
            os.makedirs(media_path, exist_ok=True)
            img_name = os.path.splitext(os.path.basename(image_url))[0] + '.webp'
            img_path = os.path.join(media_path, img_name)
            if os.path.exists(img_path):
                print(f"Изображение {obj} уже загружено {img_name}")
                return f"{folder_name}/{obj.id}/{img_name}"
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
            return f"{folder_name}/{obj.id}/{img_name}"
        except Exception as e:
            print(f"Ошибка загрузки изображения ({image_url}): {e}")
            return None

    def check_courses_for_images(self):
        base_path = Path(__file__).resolve().parent.parent.parent
        file_path = os.path.join(base_path, "files", "courses_data_clean.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for obj in data["items"]:
            course_link = obj["link"]
            course_img_link = obj["courseImage"]
            print(course_link)
            print(course_img_link)
            try:
                course = Course.objects.get(link=course_link)
            except Course.DoesNotExist:
                continue
            except Course.MultipleObjectsReturned:
                courses = Course.objects.filter(link=course_link)
                while courses.count() > 1:
                    courses.last().delete()
                course = courses.first()
            print(f"Course obj:{course}")
            img_path = self._download_and_convert_png_to_webp(course_img_link, course, "courses")
            CourseImage.objects.create(course=course, image=img_path)
            print("Done")

    def check_schools_for_images(self):
        base_path = Path(__file__).resolve().parent.parent.parent
        file_path = os.path.join(base_path, "files", "schools_data_clean.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for obj in data["items"]:
            course_link = obj["link"]
            course_img_link = obj["image"]
            print(course_link)
            print(course_img_link)
            try:
                course = Course.objects.get(link=course_link)
            except Course.DoesNotExist:
                continue
            except Course.MultipleObjectsReturned:
                courses = Course.objects.filter(link=course_link)
                while courses.count() > 1:
                    courses.last().delete()
                course = courses.first()
            print(f"Course obj:{course}")
            img_path = self._download_and_convert_png_to_webp(course_img_link, course, "courses")
            CourseImage.objects.create(course=course, image=img_path)
            print("Done")

    def load_logo_for_organizations(self):
        base_path = Path(__file__).resolve().parent.parent.parent
        file_path = os.path.join(base_path, "files", "organizations_data_clean.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for obj in data["items"]:
            alias = obj["alias"]
            logo_link = obj["logo"]
            print(alias)
            print(logo_link)

            try:
                organization = Organization.objects.get(alias=alias)
            except Organization.DoesNotExist:
                continue
            except Organization.MultipleObjectsReturned:
                organizations = Organization.objects.filter(alias=alias)
                while organizations.count() > 1:
                    organizations.last().delete()
                organization = organizations.first()

            print(f"org obj: {organization}")

            if hasattr(organization, "logo") and organization.logo:
                if organization.logo.image:
                    organization.logo.image.delete(save=False)
                organization.logo.delete()

            img_path = self._download_svg(logo_link, organization, "organizations")

            organization.logo = img_path
            organization.save()
            print("Done")