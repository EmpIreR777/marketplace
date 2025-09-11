from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    'SITE_TITLE': _('Маркет Курсов'),
    'SITE_HEADER': 'Административный сайт',
    'SITE_SUBHEADER': 'Маркет Курсов',
    'SHOW_HISTORY': True, # show/hide "History" button
    'SHOW_VIEW_ON_SITE': True, # show/hide "View on site" button
    'SHOW_BACK_BUTTON': True, # show/hide "Back" button on changeform in header
    'THEME': "dark", # Force theme: "dark" or "light"
    'SIDEBAR': {
        'show_search': True,  # Search in applications and models names
        'show_all_applications': True,  # Dropdown with all applications and models
        'navigation': [
            {
                'title': _('Администрирование'),
                'collapsible': True,
                'items': [
                    {
                        'title': _('Все пользователи'),
                        'icon': 'person',
                        'link': reverse_lazy('admin:userauth_customuser_changelist'),
                    },
                    {
                        'title': _('Администрация'),
                        'icon': 'manage_accounts',
                        'link': lambda *a: reverse_lazy('admin:userauth_customuser_changelist') + '?is_staff__exact=1',
                    },
                    {
                        'title': _('Группы'),
                        'icon': 'group',
                        'link': lambda *a: reverse_lazy('admin:auth_group_changelist') + '?is_staff__exact=1',
                    },
                ],
            },
            {
                'title': _('Студенты'),
                'collapsible': True,
                'items': [
                    {
                        'title': _('Все студенты'),
                        'icon': 'face',
                        'link': reverse_lazy('admin:student_student_changelist'),
                    },
{
                        'title': _('Подтверждённые студенты'),
                        'icon': 'add_circle',
                        'link': lambda *a: reverse_lazy('admin:student_student_changelist') + '?email_is_verified__exact=1',
                    },
{
                        'title': _('Не подтверждённые студенты'),
                        'icon': 'do_not_disturb_on',
                        'link': lambda *a: reverse_lazy('admin:student_student_changelist') + '?email_is_verified__exact=0',
                    },
                ],

            },
            {
                'title': _('Авторы'),
                'collapsible': True,
                'items': [
                    {
                        'title': _('Все авторы'),
                        'icon': 'badge',
                        'link': reverse_lazy('admin:author_author_changelist')
                    },
                    {
                        'title': _('Подтверждённые авторы'),
                        'icon': 'add_circle',
                        'link': lambda *a: reverse_lazy('admin:author_author_changelist') + '?is_verified__exact=1'
                    },
                    {
                        'title': _('Не подтверждённые авторы'),
                        'icon': 'do_not_disturb_on',
                        'link': lambda *a: reverse_lazy('admin:author_author_changelist') + '?is_verified__exact=0'
                    },
                    {
                        'title': _('Ожидающие проверки'),
                        'icon': 'pending_actions',
                        'link': lambda *a: reverse_lazy('admin:author_author_changelist') + '?verification_status__exact=ON_VERIFICATION'
                    }
                ]
            },
            {
                'title': _('Организации'),
                'collapsible': True,
                'items': [
                    {
                        'title': _('Все Организации'),
                        'icon': 'apartment',
                        'link': reverse_lazy('admin:organizations_organization_changelist')
                    },
                    {
                        'title': _('Подтверждённые организации'),
                        'icon': 'add_circle',
                        'link': lambda *a: reverse_lazy('admin:organizations_organization_changelist') + '?is_verified__exact=1'
                    },
                    {
                        'title': _('Не подтверждённые организации'),
                        'icon': 'do_not_disturb_on',
                        'link': lambda *a: reverse_lazy('admin:organizations_organization_changelist') + '?is_verified__exact=0'
                    },
                ]
            },
            {
                'title': _('Документы для авторов и организаций'),
                'collapsible': True,
                'items': [
                    {
                        'title': _('Типы Документов'),
                        'icon': 'description',
                        'link': reverse_lazy('admin:author_documenttype_changelist')
                    },
                    {
                        'title': _('Обязательные Документы'),
                        'icon': 'description',
                        'link': reverse_lazy('admin:author_requireddocument_changelist')
                    },
                ],
            },
            {
                'title': _('Курсы'),
                'collapsible': True,
                'items': [
                    {
                        'title': _('Все курсы'),
                        'icon': 'book',
                        'link': reverse_lazy('admin:courses_course_changelist'),
                    },
                    {
                        'title': _('Одобренные курсы'),
                        'icon': 'add_circle',
                        'link':lambda *a: reverse_lazy('admin:courses_course_changelist') + '?is_moderated__exact=1',
                    },
                    {
                        'title': _('Не одобренные курсы'),
                        'icon': 'do_not_disturb_on',
                        'link':lambda *a: reverse_lazy('admin:courses_course_changelist') + '?is_moderated__exact=0',
                    },
                ]
            },
            {
                'title': _('Школы'),
                'collapsible': True,
                'items': [
                    {
                        'title': _('Все школы'),
                        'icon': 'school',
                        'link': reverse_lazy('admin:courses_school_changelist'),
                    },
                    {
                        'title': _('Одобренные школы'),
                        'icon': 'add_circle',
                        'link': lambda *a: reverse_lazy('admin:courses_school_changelist') + '?is_moderated__exact=1',
                    },
                    {
                        'title': _('Не одобренные школы'),
                        'icon': 'do_not_disturb_on',
                        'link': lambda *a: reverse_lazy('admin:courses_school_changelist') + '?is_moderated__exact=0',
                    },
                ],
            },
            {
                'title': _('Характеристики курсов и школ'),
                'collapsible': True,
                'items': [
                    {
                        'title': _('Форматы'),
                        'link': reverse_lazy('admin:courses_courseformat_changelist'),
                    },
                    {
                        'title': _('Уровни'),
                        'link': reverse_lazy('admin:courses_courselevel_changelist'),
                    },
                    {
                        'title': _('Направления'),
                        'link': reverse_lazy('admin:courses_directionstype_changelist'),
                    },
                    {
                        'title': _('Тематики'),
                        'link': reverse_lazy('admin:courses_thematicstype_changelist'),
                    },
                    {
                        'title': _('Типы обучения'),

                        'link': reverse_lazy('admin:courses_learningtype_changelist'),
                    },
                    {
                        'title': _('Причины изучения'),
                        'link': reverse_lazy('admin:courses_learningreasons_changelist'),
                    },
                    {
                        'title': _('Возрастная категория'),
                        'link': reverse_lazy('admin:courses_agecategory_changelist'),
                    },
                ],
            },
            {
                'title': _('Отзывы и Комментарии'),
                'collapsible': True,
                'items': [
                    {
                        'title': _('Отзывы'),
                        'icon': 'reviews',
                        'link': reverse_lazy('admin:feedback_feedback_changelist'),
                    },
                    {
                        'title': _('Комментарии'),
                        'icon': 'chat',
                        'link': reverse_lazy('admin:feedback_comment_changelist'),
                    },
                ],
            },
            {
                'title': _('Платежи и тарифы'),
                'collapsible': True,
                'items': [
                    {
                        'title': _('Тарифы'),
                        'icon': 'receipt',
                        'link': reverse_lazy('admin:tariffs_tariff_changelist'),
                    },
                    {
                        'title': _('Оплаченные тарифы'),
                        'icon': 'receipt_long',
                        'link': reverse_lazy('admin:tariffs_usertariff_changelist'),
                    },
                    {
                        'title': _('Платежи'),
                        'icon': 'list_alt',
                        'link': reverse_lazy('admin:payments_payment_changelist'),
                    },
                ],
            },
            {
                'title': _('Обратная связь'),
                'collapsible': True,
                'items': [
                    {
                        'title': _('Обращения'),
                        'icon': 'reviews',
                        'link': reverse_lazy('admin:contacts_contact_changelist'),
                    }
                ],
            },
                        {
                'title': _('ВУЗы'),
                'collapsible': True,
                'items': [
                    {
                        'title': _('Организации ВУЗы'),
                        'icon': 'school',
                        'link': reverse_lazy('admin:vuz_organizationsvuz_changelist'),
                    },
                    {
                        'title': _('Факультеты'),
                        'icon': 'account_balance',
                        'link': reverse_lazy('admin:vuz_faculties_changelist'),
                    },
                    {
                        'title': _('Программы'),
                        'icon': 'menu_book',
                        'link': reverse_lazy('admin:vuz_programs_changelist'),
                    },
                ]
            },
            {
                'title': _('Справочники ВУЗ'),
                'collapsible': True,
                'items': [
                    {
                        'title': _('Города'),
                        'icon': 'location_city',
                        'link': reverse_lazy('admin:vuz_cities_changelist'),
                    },
                    {
                        'title': _('Субъекты РФ'),
                        'icon': 'map',
                        'link': reverse_lazy('admin:vuz_subjects_changelist'),
                    },
                    {
                        'title': _('Направления'),
                        'icon': 'category',
                        'link': reverse_lazy('admin:vuz_directions_changelist'),
                    },
                    {
                        'title': _('Специальности'),
                        'icon': 'work',
                        'link': reverse_lazy('admin:vuz_specialties_changelist'),
                    },
                    {
                        'title': _('Профессии'),
                        'icon': 'engineering',
                        'link': reverse_lazy('admin:vuz_professions_changelist'),
                    },
                    {
                        'title': _('Формы обучения'),
                        'icon': 'schedule',
                        'link': reverse_lazy('admin:vuz_forms_changelist'),
                    },
                    {
                        'title': _('Метро'),
                        'icon': 'train',
                        'link': reverse_lazy('admin:vuz_metros_changelist'),
                    },
                    {
                        'title': _('Контакты'),
                        'icon': 'contact_mail',
                        'link': reverse_lazy('admin:vuz_contacts_changelist'),
                    },
                    {
                        'title': _('Приемные комиссии'),
                        'icon': 'business_center',
                        'link': reverse_lazy('admin:vuz_admissionoffices_changelist'),
                    },
                ]
            },
            {
                'title': _('Другое'),
                'collapsible': True,
                'items': [
                    {
                        'title': _('Опросник'),
                        'icon': 'quiz',
                        'link': reverse_lazy('admin:questions_question_changelist'),
                    },
                    {
                        'title': _('Уведомления'),
                        'icon': 'notifications',
                        'link': reverse_lazy('admin:notification_notification_changelist'),
                    }
                ]
            },
        ],
    },
}