import os
from pathlib import Path
import json

from django.core.management.base import BaseCommand
from django.db import transaction
from courses.models import ThematicsType, LearningType


class Command(BaseCommand):
    help = 'Update relations between ThematicsType and LearningType based on dict_relations_all_values.json'

    def handle(self, *args, **kwargs):
        base_path = Path(__file__).resolve().parent.parent.parent
        file_path = os.path.join(base_path, "files", "dict_relations_all_values.json")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            relations = json.load(file)

        thematics_to_learning_type = {}
        for relation in relations:
            learning_type_code = relation['learningtype_code']
            thematics = relation['thematics_codes']
            for thematic in thematics:
                thematics_to_learning_type[thematic] = learning_type_code

        updated_count = 0
        not_found_thematics = []
        not_found_learning_types = set()

        with transaction.atomic():
            for thematic_name, learning_type_name in thematics_to_learning_type.items():
                try:
                    thematic = ThematicsType.objects.get(name=thematic_name)
                    learning_type, created = LearningType.objects.get_or_create(name=learning_type_name)
                    
                    if thematic.learning_type != learning_type:
                        thematic.learning_type = learning_type
                        thematic.save()
                        updated_count += 1
                        self.stdout.write(f"Updated relation: {thematic_name} -> {learning_type_name}")
                except ThematicsType.DoesNotExist:
                    not_found_thematics.append(thematic_name)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error updating {thematic_name}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS(f"\nUpdated {updated_count} relations"))
        
        if not_found_thematics:
            self.stdout.write("\nThematics not found in database:")
            for thematic in not_found_thematics:
                self.stdout.write(f"- {thematic}")

        thematics_without_learning_type = ThematicsType.objects.filter(learning_type__isnull=True)
        if thematics_without_learning_type.exists():
            self.stdout.write("\nThematics without learning type:")
            for thematic in thematics_without_learning_type:
                self.stdout.write(f"- {thematic.name}") 