from django.core.management.base import BaseCommand
from faker import Faker

from student.models import Student, StudentCoursePurchase
from userauth.models import CustomUser
from author.models import Author
from courses.models import Course
from organizations.models import Organization

fake = Faker()


class Command(BaseCommand):
    help = "Create student with courses"

    def handle(self, *args, **options):
        test_author = self.create_author()
        test_student = self.create_student()
        course_list = self.generate_author_courses(test_author)
        self.buy_courses_for_student(test_student, course_list)

    def buy_courses_for_student(self, test_student: Student, course_list: list):
        for course in course_list:
            StudentCoursePurchase.objects.get_or_create(student_profile=test_student, course=course)

    def generate_author_courses(self, test_author: Author):
        print(f"Создаем курсы для автора {test_author}")
        course_list = []
        for _ in range(3):
            try:
                course, created = Course.objects.get_or_create(
                    author=test_author,
                    name=f'Test course "{fake.sentence(nb_words=5)}"',
                    organization=Organization.objects.order_by('?').first(),
                    link=fake.url(),
                    price=fake.random_int(min=100, max=5000),
                    price_all=fake.random_int(min=5000, max=15000),
                    without_discount_price=fake.random_int(min=6000, max=20000),
                    price_installment=fake.random_int(min=500, max=3000),
                    time_installment=fake.random_int(min=1, max=24),
                    is_moderated=True,
                )
                course_list.append(course)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка при создании курса:\n"
                                                   f"{e}\n"))
                break
            self.stdout.write(self.style.SUCCESS(f"Успешно создан курс\n"
                                                 f"Course name: {course.name}\n\n"))
        else:
            self.stdout.write(self.style.SUCCESS("Генерация завершена!"))
            return course_list

    def create_author(self):
        print("Создаем тестового автора с его курсами")
        test_user, created = CustomUser.objects.get_or_create(
            email="test_author@test.com",
            defaults={
                "first_name": "Test",
                "last_name": "Author",
                "role": CustomUser.ROLE_AUTHOR,
                "is_active": True,
                "email_is_verified": True,
            }
        )
        test_user.set_password("string123")
        test_user.save()
        self.stdout.write(self.style.SUCCESS("Создан автор")) if created else None
        self.stdout.write(self.style.SUCCESS(f"Test author data:"
                                             f"\nEmail:{test_user.email}\n"
                                             f"Password:string123\n"))

        test_author, _ = Author.objects.get_or_create(
            user=test_user,
            defaults={"is_verified": True}
        )

        return test_author

    def create_student(self):
        print("Создаем тестового студента  с его курсами")
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
        return test_student
