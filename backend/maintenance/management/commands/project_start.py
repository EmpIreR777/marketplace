import os
from pathlib import Path
import random
from datetime import timedelta
import json


from django.db import transaction
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db.utils import IntegrityError
from faker import Faker

from author.models import AuthorType, LLCAuthor
from feedback.models import Feedback
from organizations.models import Organization, OrganizationRequisites
from courses.models import (
    Course,
    ThematicsType,
    CourseFormat,
    CourseLevel,
    LearningReasons,
    LearningType,
    School,
    DirectionsType
)
from student.models import Student
from userauth.models import CustomUser

faker_ = Faker()


class Command(BaseCommand):
    help = 'Project start'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thematic_relations = {}
        self.learning_types_dict = {}

    def handle(self, *args, **kwargs):
        if Organization.objects.count() > 50 and CustomUser.objects.filter(email='admin@admin.com'):
            print('Fixtures already mounted')
            return
        self.create_user()
        self.load_thematic_relations()
        self.create_all()
        self.create_questions()
        self.create_tariffs()

        call_command('get_all_verify')
        call_command('translate_types')
        call_command('load_pictures')

    def load_thematic_relations(self):
        base_path = Path(__file__).resolve().parent.parent.parent
        file_path = os.path.join(base_path, "files", "dict_relations_all_values.json")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            relations = json.load(file)
            
        for relation in relations:
            learning_type_code = relation['learningtype_code']
            thematics = relation['thematics_codes']
            self.thematic_relations[learning_type_code] = thematics

    def get_or_create_thematic(self, thematic_name, learning_type_name=None):
        learning_type = None
        for lt_code, thematics in self.thematic_relations.items():
            if thematic_name in thematics:
                learning_type, _ = LearningType.objects.get_or_create(name=lt_code)
                break
        
        if not learning_type and learning_type_name:
            learning_type, _ = LearningType.objects.get_or_create(name=learning_type_name)

        thematic, created = ThematicsType.objects.get_or_create(
            name=thematic_name,
            defaults={'learning_type': learning_type} if learning_type else {}
        )
        
        if not created and learning_type and not thematic.learning_type:
            thematic.learning_type = learning_type
            thematic.save()
            
        return thematic

    def create_user(self):
        """SuperAdmin add"""

        check_user = CustomUser.objects.filter(email='admin@admin.com')
        if not check_user:
            CustomUser.objects.create_superuser(
                email='admin@admin.com',
                first_name='admin',
                last_name='admin',
                middle_name='admin',
                password='admin',
            )
            self.stdout.write("Superuser created", ending="")

    @transaction.atomic
    def create_all(self):
        base_path = Path(__file__).resolve().parent.parent.parent

        org_dict: dict[str, Organization] = {}

        ######################################################################################################
        # Create Organizations
        ######################################################################################################

        file_path = os.path.join(base_path, "files", "organizations_data_clean.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            org_items = data.get('items')

        print('Organizations creation...')
        for i, org_data in enumerate(org_items, start=1):
            print('Organization', i)
            learning_types = org_data.pop('learning_types', [])
            learning_type_objs = []
            for learning_type_name in learning_types:
                learning_type, created = LearningType.objects.get_or_create(name=learning_type_name)
                learning_type_objs.append(learning_type)

            contacts = org_data.pop('contacts', {})
            requisites = org_data.pop('requisites', {})

            # Create organizations
            try:
                organization, created = Organization.objects.get_or_create(
                    email=contacts.get('email'),
                    defaults={
                        'first_name': faker_.first_name(),
                        'middle_name': faker_.user_name(),
                        'last_name': faker_.last_name(),
                        'title': org_data.get('name'),
                        'description': org_data.get('description'),
                        'phone_number': contacts.get('phone'),
                        'website': contacts.get('website'),
                        'address': contacts.get('address'),
                        'is_verified': True,
                        'author_type': AuthorType.ORGANIZATION,
                        'alias': org_data.get('alias'),
                        'full_title': org_data.get('fullName'),
                        'prepositional_title': org_data.get('prepositionalName'),
                        'genitive_title': org_data.get('genitiveName'),
                        'type': org_data.get('type'),
                        'partner_card': bool(org_data.get('partnerCard', False)),
                        'license': org_data.get('license'),
                        'legal_address': contacts.get('legalAddress'),
                        'personal_account_name': contacts.get('personalAccountName'),
                        'personal_account_site': contacts.get('personalAccountSite'),
                        'leadership': contacts.get('leadership'),
                        'education_type': org_data.get('additionalInfo').get('educationType'),
                        'is_premium_partner': bool(org_data.get('isPremiumPartner', False)),
                    }
                )
                if created:
                    print(f"Организация {organization.title} успешно создана")
                    LLCAuthor.objects.get_or_create(author=organization)
                else:
                    print(f"Организация с email {contacts.get('email')} уже существует")
            except IntegrityError as e:
                print(f"Ошибка создания организации: {e}")
            else:
                OrganizationRequisites.objects.get_or_create(
                    organization=organization,
                    defaults={
                        'bik': requisites.get('bik'),
                        'inn': requisites.get('inn'),
                        'kpp': requisites.get('kpp'),
                        'ogrn': requisites.get('ogrn'),
                    }
                )

                # Set many to many for Organization
                org_dict.setdefault(org_data.get('id'), organization)

        # Create Organization and Author in db
        print('Organizations creation is success.')

        ######################################################################################################
        # Create Schools
        ######################################################################################################
        file_path = os.path.join(base_path, "files", "schools_data_clean.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            school_items = data.get('items', [])

        print('Schools creation...')
        for i, school_data in enumerate(school_items, start=1):
            print('School', i)
            directions = school_data.get('directions', [])
            directions_objs = [DirectionsType.objects.get_or_create(name=d)[0] for d in directions]

            reasons = school_data.get('reasons', [])
            reasons_objs = [LearningReasons.objects.get_or_create(name=r)[0] for r in reasons]

            formats = school_data.get('formats', [])
            formats_objs = [CourseFormat.objects.get_or_create(name=f)[0] for f in formats]

            courses_thematics = school_data.get('coursesThematics', [])
            if courses_thematics is not None and courses_thematics != ["null"]:
                thematics_objs = [self.get_or_create_thematic(t) for t in courses_thematics if t is not None]
            else:
                thematics_objs = []

            org_for_school = org_dict.get(school_data.get('organization'))
            org_for_school.refresh_from_db()
            author_for_school = org_for_school if org_for_school else None
            school = School.objects.create(
                author=author_for_school,
                location=school_data.get('location', []),
                has_mentor=bool(school_data.get('isTutor', None)),
                is_demo=bool(school_data.get('isDemo', None)),
                has_parent_control=bool(school_data.get('isParentControl', None)),
                # TODO: расчитать длительность из timeDays:Month:Hours
                # time_lessons=school_data.get('timeLessons', None),

                grade_from=school_data.get('gradeFrom', None),
                grade_to=school_data.get('gradeTo', None),

                price_all=school_data.get('priceAll', None),
                price=school_data.get('price', None),
                without_discount_price=school_data.get('withoutDiscountPrice', None),
                price_installment=school_data.get('priceInstallment', None),
                time_installment=school_data.get('timeInstallment', None),
                has_free_lesson=bool(school_data.get('isFreeLesson', None)),
                has_group=bool(school_data.get('isGroup', False)),
                has_record=bool(school_data.get('hasRecord', False)),
                has_curator=bool(school_data.get('hasCurator', False)),
                has_job_guarantee=bool(school_data.get('hasGuarantee', None)),
                is_webinar=bool(school_data.get('isWebinar', None)),
            )

            # Set many to many for School
            school.directions.set(directions_objs)
            school.learning_reasons.set(reasons_objs)
            school.course_formats.set(formats_objs)
            school.courses_thematics.set(thematics_objs)

        print('Schools creation is success.')

        ######################################################################################################
        # Create Course
        ######################################################################################################
        file_path = os.path.join(base_path, "files", "courses_data_clean.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            course_items = data.get('items', [])

        print('Courses creation...')
        for i, course_data in enumerate(course_items, start=1):
            print('Course', i)
            learning_types = course_data.get('learningtype', [])
            learning_type_objs = [LearningType.objects.get_or_create(name=lt)[0] for lt in
                                  learning_types]
            thematics = course_data.get('coursesThematics', [])
            filtered_thematics = [th for th in thematics if th is not None]
            thematics_objs = [self.get_or_create_thematic(th) for th in filtered_thematics]

            formats = course_data.get('courseFormats', [])
            format_objs = [CourseFormat.objects.get_or_create(name=fmt)[0] for fmt in formats]

            levels = course_data.get('courseLevels', [])
            level_objs = [CourseLevel.objects.get_or_create(name=lv)[0] for lv in levels]

            targets = course_data.get('courseTargets', [])
            learning_reasons_objs = [LearningReasons.objects.get_or_create(name=tg)[0]
                                     for tg in targets]

            org_for_school = org_dict.get(course_data.get('organization'))
            author_for_school = org_for_school if org_for_school else None
            course = Course.objects.create(
                author=author_for_school,
                name=course_data.get('name'),
                link=course_data.get('link'),

                price=course_data.get('price'),
                price_all=course_data.get('priceAll'),
                without_discount_price=course_data.get('withoutDiscountPrice'),
                price_installment=course_data.get('priceInstallment'),
                time_installment=course_data.get('timeInstallment'),

                duration=timedelta(hours=course_data.get('courseDuration')),
                is_duration_approximately=bool(course_data.get('isTermApproximately')),

                portfolio_text=course_data.get('portfolioText'),
                provides_diploma=bool(course_data.get('diploma')),
                diploma_content=course_data.get('diplomaContent'),
                has_mentor=bool(course_data.get('mentor')),
                has_job_help=bool(course_data.get('jobHelp')),
                has_job_guarantee=bool(course_data.get('jobGarant')),
                is_webinar=bool(course_data.get('isWebinar')),
                is_top_sale=bool(course_data.get('isTopSale')),
                is_wow_effect=bool(course_data.get('isWowEffect')),
                description=course_data.get('courseDescription'),
                is_moderated=True,
            )

            # Set the many-to-many relationships
            course.learning_types.set(learning_type_objs)
            course.courses_thematics.set(thematics_objs)
            course.course_formats.set(format_objs)
            course.course_levels.set(level_objs)
            course.learning_reasons.set(learning_reasons_objs)

        print('Courses creation is success.')
        ######################
        # create 100 students
        for i in range(100):
            Student.objects.create(
                email=faker_.email(),
                first_name=faker_.first_name(),
                middle_name=faker_.user_name(),
                last_name=faker_.last_name(),
            )
        ######################################################################################################
        # Create Feedbacks
        ######################################################################################################
        students_pk_list = Student.objects.values_list('pk', flat=True)
        courses = Course.objects.all()
        print('Feedbacks creation...')
        with transaction.atomic():
            feedbacks = []
            count = 1
            for course in courses:
                for _ in range(random.randint(3, 10)):
                    print('Feedback', count)
                    feedbacks.append(
                        Feedback(
                            feedback_author=Student.objects.get(pk=random.choice(students_pk_list)),
                            feedback_to_course=course,
                            feedback_text=faker_.text(),
                            feedback_rating=random.randint(1, 5),
                            is_approved=True,
                        )
                    )
                    count += 1
            Feedback.objects.bulk_create(feedbacks)

        print('Feedbacks creation is success.')

    def create_questions(self):
        """Создание вопросов из JSON файла"""

        call_command("loaddata", "maintenance/files/questions.json")

    def create_tariffs(self):
        """Создание тарифов из JSON файла"""
        call_command('loaddata', 'maintenance/files/tariffs.json')
