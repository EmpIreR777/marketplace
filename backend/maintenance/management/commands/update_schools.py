import os
from pathlib import Path
import json
from typing import Dict, Any, Optional

from django.core.management.base import BaseCommand
from django.db import transaction
from courses.models import School
from django.db.models import Q


class Command(BaseCommand):
    help = 'Update schools names and descriptions from schools_data_clean.json'

    def get_match_score(self, school: School, school_data: Dict[Any, Any]) -> Optional[float]:
        """
        Вычисляет score соответствия между школой из БД и данными из JSON.
        Возвращает None если школы точно не совпадают, иначе возвращает score от 0 до 1.
        """
        score = 0
        total_checks = 0

        bool_fields = [
            ('has_mentor', 'isTutor'),
            ('is_demo', 'isDemo'),
            ('has_parent_control', 'isParentControl'),
            ('has_free_lesson', 'isFreeLesson'),
            ('has_group', 'isGroup'),
            ('has_record', 'hasRecord'),
            ('has_curator', 'hasCurator'),
            ('has_job_guarantee', 'hasGuarantee'),
            ('is_webinar', 'isWebinar'),
        ]
        
        for db_field, json_field in bool_fields:
            json_value = school_data.get(json_field)
            if json_value is not None:
                total_checks += 1
                if getattr(school, db_field) == bool(json_value):
                    score += 1

        numeric_fields = [
            ('grade_from', 'gradeFrom'),
            ('grade_to', 'gradeTo'),
            ('price', 'price'),
            ('price_all', 'priceAll'),
            ('without_discount_price', 'withoutDiscountPrice'),
            ('price_installment', 'priceInstallment'),
            ('time_installment', 'timeInstallment'),
        ]

        for db_field, json_field in numeric_fields:
            json_value = school_data.get(json_field)
            if json_value is not None:
                total_checks += 1
                if getattr(school, db_field) == json_value:
                    score += 1

        if school.location == school_data.get('location', []):
            score += 1
            total_checks += 1

        if (school.author and 
            school.author.email and 
            school_data.get('contacts', {}).get('email') and
            any(email in school_data['contacts']['email'] for email in [school.author.email])):
            score += 2
            total_checks += 2

        if total_checks == 0:
            return None

        return score / total_checks

    def handle(self, *args, **kwargs):
        base_path = Path(__file__).resolve().parent.parent.parent
        file_path = os.path.join(base_path, "files", "schools_data_clean.json")

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            school_items = data.get('items', [])

        updated_count = 0
        schools_without_match = []
        matched_schools = {}  

        with transaction.atomic():
            schools = School.objects.select_related('author').all()
            
            for school in schools:
                best_match = None
                best_score = 0

                for school_data in school_items:
                    score = self.get_match_score(school, school_data)
                    if score and score > best_score:
                        best_score = score
                        best_match = school_data

                if best_score > 0.7:
                    matched_schools[school.id] = best_match
                else:
                    schools_without_match.append(school)

            for school in schools:
                matching_data = matched_schools.get(school.id)
                if matching_data:
                    was_updated = False
                    
                    if not school.name and matching_data.get('name'):
                        school.name = matching_data['name']
                        was_updated = True
                    
                    if not school.description and matching_data.get('description'):
                        school.description = matching_data['description']
                        was_updated = True
                    
                    if was_updated:
                        school.save()
                        updated_count += 1
                        self.stdout.write(f"Updated school: {school.name} (match score: {best_score:.2f})")

        self.stdout.write(self.style.SUCCESS(f"\nUpdated {updated_count} schools"))
        
        if schools_without_match:
            self.stdout.write("\nSchools without matching data in JSON:")
            for school in schools_without_match:
                self.stdout.write(
                    f"- ID: {school.id}\n"
                    f"  Current name: {school.name}\n"
                    f"  Author email: {school.author.email if school.author else 'No author'}\n"
                    f"  Location: {school.location}\n"
                    f"  Grades: {school.grade_from}-{school.grade_to}"
                )

        schools_without_name = School.objects.filter(name__isnull=True)
        schools_without_description = School.objects.filter(description__isnull=True)

        if schools_without_name.exists():
            self.stdout.write("\nSchools without names:")
            for school in schools_without_name:
                self.stdout.write(f"- ID: {school.id}, Author: {school.author.email if school.author else 'No author'}")

        if schools_without_description.exists():
            self.stdout.write("\nSchools without descriptions:")
            for school in schools_without_description:
                self.stdout.write(f"- ID: {school.id}, Name: {school.name}, Author: {school.author.email if school.author else 'No author'}") 