import os
import json
from django.core.management.base import BaseCommand
from pathlib import Path
from courses.models import (
    DirectionsType,
    LearningType,
    ThematicsType,
    CourseFormat,
    CourseLevel,
    LearningReasons,
    AgeCategory
)

class Command(BaseCommand):
    help = 'Import translations from JSON file to database'

    def handle(self, *args, **options):
        base_path = Path(__file__).resolve().parent.parent.parent
        file_path = os.path.join(base_path, "files", "dict_kor.json")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        translations_data = {
            'Направления обучения': {},
            'Категории курсов': {},
            'Тематики курсов': {},
            'Формат курса': {},
            'Уровень курса': {},
            'Цели подготовки': {},
            'Школьные классы': {}
        }

        for item in data['data']['directions']['fields']:
            translations_data['Направления обучения'][item['value']] = item['name']

        for item in data['data']['learningtype']['fields']:
            translations_data['Категории курсов'][item['value']] = item['name']
        
        for item in data['data']['coursesThematics']['fields']:
            translations_data['Тематики курсов'][item['value']] = item['name']
        
        for item in data['data']['courseFormats']['fields']:
            translations_data['Формат курса'][item['value']] = item['name']
        
        for item in data['data']['courseLevels']['fields']:
            translations_data['Уровень курса'][item['value']] = item['name']
        
        for item in data['data']['reasons']['fields']:
            translations_data['Цели подготовки'][item['value']] = item['name']
        
        for item in data['data']['schoolGrades']['fields']:
            translations_data['Школьные классы'][item['value']] = item['name']


        self.update_translations(DirectionsType, translations_data.get('Направления обучения', {}))
        self.update_translations(LearningType, translations_data.get('Категории курсов', {}))
        self.update_translations(ThematicsType, translations_data.get('Тематики курсов', {}))
        self.update_translations(CourseFormat, translations_data.get('Формат курса', {}))
        self.update_translations(CourseLevel, translations_data.get('Уровень курса', {}))
        self.update_translations(LearningReasons, translations_data.get('Цели подготовки', {}))
        self.update_translations(AgeCategory, translations_data.get('Школьные классы', {}))
        
        self.stdout.write(self.style.SUCCESS('Successfully updated translations from JSON'))

    def update_translations(self, model, translations_dict):
        for obj in model.objects.all():
            if obj.name in translations_dict:
                obj.translations = translations_dict[obj.name]
                obj.save()
            else:
                for value, translation in translations_dict.items():
                    if value.lower() in obj.name.lower() or obj.name.lower() in translation.lower():
                        obj.translations = translation
                        obj.save()
                        break