import os
import json
from pathlib import Path
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction, connection
from django.utils import timezone

from vuz.models import (
    AdmissionOffices, Cities, Contacts, 
    Directions, DirectionsOrganizations,
    Metros, Subjects, OrganizationsVuz,
    Faculties, Forms, Professions,
    ProfessionsOrganizations, Specialties,
    SpecialtiesOrganizations, Programs
)

class Command(BaseCommand):
    help = 'Загрузка данных для приложения VUZ из JSON-файлов'

    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            type=str,
            help='Название модели для загрузки (например, cities). Если не указано, загрузятся все модели.'
        )
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Сбросить таблицы перед загрузкой данных'
        )

    def _parse_datetime(self, date_str):
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str)
        except (ValueError, TypeError):
            return None

    def _load_data_for_model(self, model_class, json_file, relation_fields=None):
        if relation_fields is None:
            relation_fields = {}
            
        base_path = Path(__file__).resolve().parent.parent.parent
        file_path = os.path.join(base_path, "files", "vuz", json_file)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                
                data = None
                
                model_name_lower = model_class.__name__.lower()
                
                if model_name_lower in json_data:
                    data = json_data[model_name_lower]
                elif json_file.split('.')[0] in json_data:
                    data = json_data[json_file.split('.')[0]]
                else:
                    data = json_data
                
                if isinstance(data, str):
                    self.stdout.write(self.style.ERROR(f"Файл {file_path} содержит строку вместо JSON-объекта"))
                    return
                elif not isinstance(data, list):
                    if isinstance(data, dict) and not any(isinstance(data[key], dict) for key in data):
                        data = [data]
                    else:
                        self.stdout.write(self.style.WARNING(f"Данные в {file_path} не являются списком, попытка извлечь объекты"))
                        extracted_data = []
                        for key, value in data.items():
                            if isinstance(value, dict):
                                extracted_data.append(value)
                        if extracted_data:
                            data = extracted_data
                        else:
                            data = [data]
                
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Файл {file_path} не найден"))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f"Файл {file_path} содержит невалидный JSON"))
            return
        
        model_name = model_class.__name__
        total_items = len(data)
        created_count = 0
        updated_count = 0
        error_count = 0
        
        self.stdout.write(f"Загрузка {total_items} записей для модели {model_name}")
        
        with transaction.atomic():
            for index, item in enumerate(data):
                if not isinstance(item, dict):
                    self.stdout.write(self.style.ERROR(f"Элемент {index} не является словарем: {item}"))
                    error_count += 1
                    continue
                    
                if index % 1000 == 0 and index > 0:
                    self.stdout.write(f"Обработано {index}/{total_items} записей...")
                
                item_data = item.copy()
                
                model_fields = [field.name for field in model_class._meta.fields]
                model_field_objects = {field.name: field for field in model_class._meta.fields}
                
                for field in model_class._meta.fields:
                    if field.is_relation:
                        if field.name not in model_fields:
                            model_fields.append(field.name)
                        field_id = f"{field.name}_id"
                        if field_id not in model_fields:
                            model_fields.append(field_id)
                
                item_data = {key: value for key, value in item_data.items() if key in model_fields}
                
                if 'phones' in item_data:
                    phones_value = item_data['phones']
                    if isinstance(phones_value, str):
                        if phones_value.startswith('{') and phones_value.endswith('}'):
                            phones_content = phones_value[1:-1]  # удаляем фигурные скобки
                            
                            if '"' in phones_content:
                                phones_items = []
                                in_quotes = False
                                current_item = ""
                                
                                for char in phones_content:
                                    if char == '"':
                                        in_quotes = not in_quotes
                                    elif char == ',' and not in_quotes:
                                        if current_item:
                                            phones_items.append(current_item.strip('"').strip())
                                            current_item = ""
                                    else:
                                        current_item += char
                                
                                if current_item:
                                    phones_items.append(current_item.strip('"').strip())
                                
                                item_data['phones'] = phones_items
                            else:
                                phones_list = [phone.strip() for phone in phones_content.split(',')]
                                item_data['phones'] = phones_list
                        elif phones_value.startswith('[') and phones_value.endswith(']'):
                            try:
                                item_data['phones'] = json.loads(phones_value)
                            except json.JSONDecodeError:
                                pass
                
                for field_name, field_value in list(item_data.items()):
                    if field_name in model_field_objects:
                        field_obj = model_field_objects[field_name]
                        field_type = field_obj.__class__.__name__
                        
                        if field_type in ['JSONField', 'TextField'] and isinstance(field_value, str):
                            if field_value.startswith('{') and field_value.endswith('}') or \
                               field_value.startswith('[') and field_value.endswith(']'):
                                try:
                                    item_data[field_name] = json.loads(field_value)
                                except json.JSONDecodeError:
                                    pass
                
                for field in ['created_at', 'updated_at', 'external_updated_at', 'confirmed_and_date', 
                              'licence_date', 'accreditation_date', 'start_date', 'end_date']:
                    if field in item_data:
                        item_data[field] = self._parse_datetime(item_data[field])
                
                for field, (related_model, lookup_field) in relation_fields.items():
                    if field in item_data and item_data[field]:
                        try:
                            related_obj = related_model.objects.get(**{lookup_field: item_data[field]})
                            item_data[field] = related_obj
                        except related_model.DoesNotExist:
                            self.stdout.write(self.style.WARNING(
                                f"Связанный объект {related_model.__name__} с {lookup_field}={item_data[field]} не найден"
                            ))
                            item_data[field] = None
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(
                                f"Ошибка при поиске связанного объекта {related_model.__name__}: {e}"
                            ))
                            item_data[field] = None

                try:
                    if 'created_at' in model_fields and 'created_at' not in item_data:
                        item_data['created_at'] = timezone.now()
                    if 'updated_at' in model_fields and 'updated_at' not in item_data:
                        item_data['updated_at'] = timezone.now()
                    
                    if 'created_at' in item_data and 'created_at' not in model_fields:
                        del item_data['created_at']
                    if 'updated_at' in item_data and 'updated_at' not in model_fields:
                        del item_data['updated_at']
                    
                    boolean_fields = [
                        'published', 'is_state', 'is_hostel', 'is_military', 'is_departmental', 
                        'is_partner', 'has_leads', 'is_confirmed', 'is_top100', 'is_full_year',
                        'is_capital', 'obrnadzor_checked'
                    ]
                    
                    for field in boolean_fields:
                        if field in model_fields and field in item_data and item_data[field] is None:
                            item_data[field] = False
                    
                    if 'id' in item_data and item_data['id']:
                        filter_params = {'id': item_data['id']}
                        if 'type' in item_data and 'source' in item_data:
                            filter_params['type'] = item_data['type']
                            filter_params['source'] = item_data['source']
                            
                        obj, created = model_class.objects.update_or_create(
                            **filter_params,
                            defaults=item_data
                        )
                        
                        if created:
                            created_count += 1
                        else:
                            updated_count += 1
                    else:
                        obj, created = model_class.objects.get_or_create(**item_data)
                        if created:
                            created_count += 1
                        else:
                            updated_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Ошибка при обработке записи {item_data}: {str(e)}"))
                    error_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f"{model_name}: создано {created_count}, обновлено {updated_count}, ошибок {error_count}"
        ))

    def handle(self, *args, **options):
        model = options.get('model')
        reset = options.get('reset')
        
        if reset:
            self.stdout.write("Сброс таблиц перед загрузкой данных...")
            with connection.cursor() as cursor:
                cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
                
                tables = [
                    'programs', 'specialties_organizations', 'professions_organizations', 
                    'directions_organizations', 'faculties', 'organizations_vuz',
                    'admission_offices', 'vuz_contacts', 'subjects', 'metros', 'cities',
                    'forms', 'directions', 'professions', 'specialties'
                ]
                
                for table in tables:
                    try:
                        self.stdout.write(f"Очистка таблицы {table}...")
                        cursor.execute(f"TRUNCATE TABLE {table};")
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"Ошибка при очистке таблицы {table}: {str(e)}"))
                
                cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
        
        model_loaders = {
            'cities': {
                'model': Cities,
                'file': 'cities.json',
                'relations': {}
            },
            'metros': {
                'model': Metros,
                'file': 'metros.json',
                'relations': {}
            },
            'subjects': {
                'model': Subjects,
                'file': 'subjects.json',
                'relations': {}
            },
            'contacts': {
                'model': Contacts,
                'file': 'contacts.json',
                'relations': {}
            },
            'admission_offices': {
                'model': AdmissionOffices,
                'file': 'admission_offices.json',
                'relations': {}
            },
            'organizations_vuz': {
                'model': OrganizationsVuz,
                'file': 'organizations_vuz.json',
                'relations': {
                    'city': (Cities, 'id'),
                    'subject': (Subjects, 'id'),
                    'metro': (Metros, 'id'),
                    'contact': (Contacts, 'id'),
                    'admission_office': (AdmissionOffices, 'id')
                }
            },
            'directions': {
                'model': Directions,
                'file': 'directions.json',
                'relations': {}
            },
            'directions_organizations': {
                'model': DirectionsOrganizations,
                'file': 'directions_organizations.json',
                'relations': {
                    'direction': (Directions, 'id'),
                    'organization_vuz': (OrganizationsVuz, 'id')
                }
            },
            'faculties': {
                'model': Faculties,
                'file': 'faculties.json',
                'relations': {
                    'organization_vuz': (OrganizationsVuz, 'id')
                }
            },
            'forms': {
                'model': Forms,
                'file': 'forms.json',
                'relations': {}
            },
            'professions': {
                'model': Professions,
                'file': 'professions.json',
                'relations': {}
            },
            'professions_organizations': {
                'model': ProfessionsOrganizations,
                'file': 'professions_organizations.json',
                'relations': {
                    'profession': (Professions, 'id'),
                    'organization_vuz': (OrganizationsVuz, 'id')
                }
            },
            'specialties': {
                'model': Specialties,
                'file': 'specialties.json',
                'relations': {}
            },
            'specialties_organizations': {
                'model': SpecialtiesOrganizations,
                'file': 'specialties_organizations.json',
                'relations': {
                    'specialty': (Specialties, 'id'),
                    'organization_vuz': (OrganizationsVuz, 'id')
                }
            },
            'programs': {
                'model': Programs,
                'file': 'programs.json',
                'relations': {
                    'organization_vuz': (OrganizationsVuz, 'id'),
                    'faculty': (Faculties, 'id'),
                    'specialty': (Specialties, 'id'),
                    'form': (Forms, 'id')
                }
            }
        }
        
        start_time = timezone.now()
        
        if model:
            if model in model_loaders:
                loader = model_loaders[model]
                self.stdout.write(f"Загрузка данных только для модели {model}")
                self._load_data_for_model(
                    loader['model'], 
                    loader['file'], 
                    loader['relations']
                )
            else:
                self.stdout.write(self.style.ERROR(
                    f"Модель '{model}' не найдена. Доступные модели: {', '.join(model_loaders.keys())}"
                ))
        else:
            self.stdout.write("Загрузка данных для всех моделей в приложении vuz")
            
            for model_name, loader in model_loaders.items():
                self.stdout.write(f"\nЗагрузка данных для модели {model_name}")
                self._load_data_for_model(
                    loader['model'], 
                    loader['file'], 
                    loader['relations']
                )
        
        end_time = timezone.now()
        duration = end_time - start_time
        self.stdout.write(self.style.SUCCESS(f"Загрузка данных завершена за {duration}")) 