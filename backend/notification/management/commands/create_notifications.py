import random
from faker import Faker
from django.core.management.base import BaseCommand

from student.models import Student
from userauth.models import CustomUser
from notification.models import Notification, NotificationTypes

fake = Faker()


class Command(BaseCommand):
    help = "Generate random 5 notifications for test student users"

    def handle(self, *args, **options):
        test_student = self.create_user_student()
        self.create_notifications(test_student)

    def create_notifications(self, user: CustomUser):
        for _ in range(10):
            try:
                notification_type = random.choice(NotificationTypes.choices)
                nt = Notification.objects.create(
                    user=user,
                    title=notification_type[1],
                    notification_type=notification_type[0],
                    body=fake.paragraph(nb_sentences=3),
                    html=f"<p>{fake.paragraph(nb_sentences=3)}</p>",
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка при создании:\n"
                                                   f"{e}\n"))
                break
            else:
                self.stdout.write(self.style.SUCCESS(f"Создано уведомление {nt.title}"))
        else:
            self.stdout.write(self.style.SUCCESS("Завершено успешно"))

    def create_user_student(self) -> CustomUser:
        print("Создаем тестового студента")
        test_user, created = CustomUser.objects.get_or_create(
            email="student@student.com",
            defaults={
                "first_name": "Test",
                "last_name": "Student",
                "role": CustomUser.ROLE_STUDENT,
                "is_active": True,
            }
        )
        test_user.set_password("string123")
        self.stdout.write(self.style.SUCCESS("Создан студент")) if created else None
        test_user.save()
        self.stdout.write(self.style.SUCCESS(f"Test student data:"
                                             f"\nEmail:{test_user.email}\n"
                                             f"Password:string123\n"))
        test_student, _ = Student.objects.get_or_create(
            user=test_user,
        )
        return test_user
