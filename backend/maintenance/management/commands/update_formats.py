from django.core.management.base import BaseCommand
from django.db import transaction
from courses.models import Course, CourseFormat


class Command(BaseCommand):
    help = 'Update course formats to standardized values (offline, online, record)'

    def handle(self, *args, **kwargs):
        format_mapping = {
            'formatOffline': 'offline',
            'formatOnline': 'online',
        }

        updated_count = 0

        with transaction.atomic():
            for old_format, new_format in format_mapping.items():
                old_formats = CourseFormat.objects.filter(name=old_format)
                if old_formats.exists():
                    old_format_obj = old_formats.first()
                    new_format_obj, created = CourseFormat.objects.get_or_create(name=new_format)
                    
                    courses = Course.objects.filter(course_formats=old_format_obj)
                    count = courses.count()
                    
                    if count > 0:
                        for course in courses:
                            course.course_formats.remove(old_format_obj)
                            course.course_formats.add(new_format_obj)
                        
                        updated_count += count
                        self.stdout.write(f"Updated {count} courses from {old_format} to {new_format}")
                        
                        if not Course.objects.filter(course_formats=old_format_obj).exists():
                            old_format_obj.delete()
                            self.stdout.write(f"Deleted unused format: {old_format}")

        self.stdout.write(
            self.style.SUCCESS(f"\nSuccessfully updated {updated_count} course formats")
        )

        self.stdout.write("\nCurrent course format distribution:")
        for format_obj in CourseFormat.objects.all():
            count = Course.objects.filter(course_formats=format_obj).count()
            self.stdout.write(f"- {format_obj.name}: {count} courses") 