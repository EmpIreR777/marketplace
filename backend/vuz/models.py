from django.db import models
from django.utils.translation import gettext_lazy as _


class AdmissionOffices(models.Model):
    id = models.AutoField(verbose_name=_('ID'), primary_key=True)
    type = models.CharField(verbose_name=_('Тип'), max_length=50)
    source = models.CharField(verbose_name=_('Источник'), max_length=50)
    site = models.CharField(verbose_name=_('Сайт'), max_length=255, blank=True, null=True)
    email = models.CharField(verbose_name=_('Email'), max_length=100, blank=True, null=True)
    phones = models.JSONField(verbose_name=_('Телефоны'), blank=True, null=True)
    address = models.CharField(verbose_name=_('Адрес'), max_length=1000, blank=True, null=True)
    longitude_latitude = models.CharField(verbose_name=_('Координаты'), max_length=50, blank=True, null=True)
    post_index = models.CharField(verbose_name=_('Почтовый индекс'), max_length=10, blank=True, null=True)
    schedule = models.JSONField(verbose_name=_('Расписание работы'), blank=True, null=True)
    description = models.CharField(verbose_name=_('Описание работы'), max_length=500, blank=True, null=True)
    start_date = models.DateTimeField(verbose_name=_('Дата начала работы'), blank=True, null=True)
    end_date = models.DateTimeField(verbose_name=_('Дата окончания работы'), blank=True, null=True)
    is_full_year = models.BooleanField(verbose_name=_('Работает весь год'))
    created_at = models.DateTimeField(verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(verbose_name=_('Дата обновления'))
    external_updated_at = models.DateTimeField(verbose_name=_('Дата внешнего обновления'), blank=True, null=True)

    class Meta:
        db_table = 'admission_offices'
        unique_together = (('id', 'type', 'source'),)
        verbose_name = _('Приемная комиссия')
        verbose_name_plural = _('Приемные комиссии')


class Cities(models.Model):
    id = models.AutoField(verbose_name=_('ID'), primary_key=True)
    type = models.CharField(verbose_name=_('Тип'), max_length=50)
    source = models.CharField(verbose_name=_('Источник'), max_length=50)
    name = models.CharField(verbose_name=_('Название'), max_length=255)
    name_rp = models.CharField(verbose_name=_('Название в родительном падеже'), max_length=255, blank=True, null=True)
    is_capital = models.BooleanField(verbose_name=_('Является столицей'))
    city_type = models.CharField(verbose_name=_('Тип населенного пункта'), max_length=50, blank=True, null=True)
    ratio_population = models.CharField(verbose_name=_('Категория по населению'), max_length=50, blank=True, null=True)
    fias_id = models.CharField(verbose_name=_('Идентификатор ФИАС'), max_length=50, blank=True, null=True)
    kladr_id = models.CharField(verbose_name=_('Идентификатор КЛАДР'), max_length=50, blank=True, null=True)
    longitude_latitude = models.CharField(verbose_name=_('Координаты'), max_length=50, blank=True, null=True)
    calculation_data = models.JSONField(verbose_name=_('Расчетные данные по городу'), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(verbose_name=_('Дата обновления'))

    class Meta:
        db_table = 'cities'
        unique_together = (('id', 'type', 'source'),)
        verbose_name = _('Город')
        verbose_name_plural = _('Города')


class Contacts(models.Model):
    id = models.AutoField(verbose_name=_('ID'), primary_key=True)
    type = models.CharField(verbose_name=_('Тип'), max_length=50)
    source = models.CharField(verbose_name=_('Источник'), max_length=50)
    post_index = models.CharField(verbose_name=_('Почтовый индекс'), max_length=20, blank=True, null=True)
    address = models.CharField(verbose_name=_('Адрес'), max_length=500, blank=True, null=True)
    site = models.CharField(verbose_name=_('Веб-сайт'), max_length=255, blank=True, null=True)
    phones = models.TextField(verbose_name=_('Список телефонов'), blank=True, null=True)
    email = models.CharField(verbose_name=_('Email адрес'), max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(verbose_name=_('Дата обновления'))

    class Meta:
        db_table = 'vuz_contacts'
        unique_together = (('id', 'type', 'source'),)
        verbose_name = _('Контакт')
        verbose_name_plural = _('Контакты')


class Directions(models.Model):
    id = models.AutoField(verbose_name=_('ID'), primary_key=True)
    type = models.CharField(verbose_name=_('Тип'), max_length=50)
    source = models.CharField(verbose_name=_('Источник'), max_length=50)
    name = models.CharField(verbose_name=_('Название направления'), max_length=255)
    code = models.CharField(verbose_name=_('Код направления'), max_length=20, blank=True, null=True)
    synonym = models.CharField(verbose_name=_('Синоним'), max_length=100, blank=True, null=True)
    organization_type = models.CharField(verbose_name=_('Тип организации'), max_length=50, blank=True, null=True)
    calculation_data = models.JSONField(verbose_name=_('Расчетные параметры направления'), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(verbose_name=_('Дата обновления'))

    class Meta:
        db_table = 'directions'
        unique_together = (('id', 'type', 'source'),)
        verbose_name = _('Направление')
        verbose_name_plural = _('Направления')


class DirectionsOrganizations(models.Model):
    direction = models.ForeignKey(Directions, models.DO_NOTHING, to_field='id', verbose_name=_('Направление'))
    organization_vuz = models.ForeignKey('OrganizationsVuz', models.DO_NOTHING, to_field='id', verbose_name=_('ВУЗ'))

    class Meta:
        db_table = 'directions_organizations'
        unique_together = (('direction', 'organization_vuz'),)
        verbose_name = _('Направление ВУЗа')
        verbose_name_plural = _('Направления ВУЗов')


class Metros(models.Model):
    id = models.AutoField(verbose_name=_('ID'), primary_key=True)
    type = models.CharField(verbose_name=_('Тип'), max_length=50)
    source = models.CharField(verbose_name=_('Источник'), max_length=50)
    name = models.CharField(verbose_name=_('Название'), max_length=255)
    created_at = models.DateTimeField(verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(verbose_name=_('Дата обновления'))

    class Meta:
        db_table = 'metros'
        unique_together = (('id', 'type', 'source'),)
        verbose_name = _('Станция метро')
        verbose_name_plural = _('Станции метро')


class Subjects(models.Model):
    id = models.AutoField(verbose_name=_('ID'), primary_key=True)
    type = models.CharField(verbose_name=_('Тип'), max_length=50)
    source = models.CharField(verbose_name=_('Источник'), max_length=50)
    name = models.CharField(verbose_name=_('Название'), max_length=255, blank=True, null=True)
    name_rp = models.CharField(verbose_name=_('Название в родительном падеже'), max_length=255, blank=True, null=True)
    code = models.CharField(verbose_name=_('Код'), max_length=10, blank=True, null=True)
    subject_type = models.CharField(verbose_name=_('Тип области'), max_length=50, blank=True, null=True)
    fias_id = models.CharField(verbose_name=_('Идентификатор ФИАС'), max_length=50, blank=True, null=True)
    kladr_id = models.CharField(verbose_name=_('Идентификатор КЛАДР'), max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(verbose_name=_('Дата обновления'))

    class Meta:
        db_table = 'subjects'
        unique_together = (('id', 'type', 'source'),)
        verbose_name = _('Область')
        verbose_name_plural = _('Области')


class OrganizationsVuz(models.Model):
    id = models.AutoField(verbose_name=_('ID'), primary_key=True)
    type = models.CharField(verbose_name=_('Тип'), max_length=50)
    source = models.CharField(verbose_name=_('Источник'), max_length=50)
    name = models.CharField(verbose_name=_('Название'), max_length=500)
    code = models.CharField(verbose_name=_('Код'), max_length=50, blank=True, null=True)
    full_name = models.CharField(verbose_name=_('Полное название'), max_length=500, blank=True, null=True)
    short_name = models.CharField(verbose_name=_('Краткое название'), max_length=500, blank=True, null=True)
    obrnadzor_name = models.CharField(verbose_name=_('Название в Обрнадзоре'), max_length=500, blank=True, null=True)
    obrnadzor_checked = models.BooleanField(verbose_name=_('Проверено Обрнадзором'), blank=True, null=True)
    short_seo = models.CharField(verbose_name=_('SEO краткое название'), blank=True, null=True)
    about = models.TextField(verbose_name=_('О ВУЗе'), blank=True, null=True)
    logo = models.CharField(verbose_name=_('Логотип'), blank=True, null=True)
    logo_storage = models.CharField(verbose_name=_('Хранилище логотипа'), blank=True, null=True)
    video_link = models.CharField(verbose_name=_('Ссылка на видео'), blank=True, null=True)
    sort = models.IntegerField(verbose_name=_('Сортировка'), blank=True, null=True)
    sort_for_region = models.IntegerField(verbose_name=_('Сортировка для региона'), blank=True, null=True)
    sort_for_top = models.IntegerField(verbose_name=_('Сортировка для топа'), blank=True, null=True)
    inn = models.CharField(verbose_name=_('ИНН'), blank=True, null=True)
    kpp = models.CharField(verbose_name=_('КПП'), blank=True, null=True)
    monitoring_code = models.CharField(verbose_name=_('Код мониторинга'), blank=True, null=True)
    longitude_latitude = models.CharField(verbose_name=_('Координаты'), blank=True, null=True)
    organization_type = models.CharField(verbose_name=_('Тип организации'), blank=True, null=True)
    sub_type = models.CharField(verbose_name=_('Подтип'), blank=True, null=True)
    site = models.CharField(verbose_name=_('Сайт'), blank=True, null=True)
    published = models.BooleanField(verbose_name=_('Опубликовано'))
    is_state = models.BooleanField(verbose_name=_('Государственный'))
    is_hostel = models.BooleanField(verbose_name=_('Есть общежитие'))
    is_military = models.BooleanField(verbose_name=_('Военный'))
    is_departmental = models.BooleanField(verbose_name=_('Ведомственный'))
    is_partner = models.BooleanField(verbose_name=_('Партнер'))
    has_leads = models.BooleanField(verbose_name=_('Есть лиды'))
    is_confirmed = models.BooleanField(verbose_name=_('Подтвержден'))
    licence_num = models.CharField(verbose_name=_('Номер лицензии'), blank=True, null=True)
    licence_date = models.DateTimeField(verbose_name=_('Дата лицензии'), blank=True, null=True)
    accreditation_number = models.CharField(verbose_name=_('Номер аккредитации'), blank=True, null=True)
    accreditation_date = models.DateTimeField(verbose_name=_('Дата аккредитации'), blank=True, null=True)
    rating = models.FloatField(verbose_name=_('Рейтинг'), blank=True, null=True)
    esi = models.FloatField(verbose_name=_('ЕСИ'), blank=True, null=True)
    esi24 = models.CharField(verbose_name=_('ЕСИ24'), blank=True, null=True)
    esi_marks = models.FloatField(verbose_name=_('Оценки ЕСИ'), blank=True, null=True)
    is_top100 = models.BooleanField(verbose_name=_('Топ 100'))
    ege_score = models.CharField(verbose_name=_('Балл ЕГЭ'), blank=True, null=True)
    cost = models.IntegerField(verbose_name=_('Стоимость'), blank=True, null=True)
    old_names = models.TextField(verbose_name=_('Старые названия'), blank=True, null=True)
    delete_reason = models.CharField(verbose_name=_('Причина удаления'), blank=True, null=True)
    confirmed_and_date = models.DateTimeField(verbose_name=_('Дата подтверждения'), blank=True, null=True)
    calculation_data = models.JSONField(verbose_name=_('Расчетные параметры организации'), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(verbose_name=_('Дата обновления'))
    external_updated_at = models.DateTimeField(verbose_name=_('Дата внешнего обновления'), blank=True, null=True)
    admission_office = models.OneToOneField(AdmissionOffices, models.DO_NOTHING, blank=True, null=True, verbose_name=_('Приемная комиссия'))
    contact = models.OneToOneField(Contacts, models.DO_NOTHING, blank=True, null=True, verbose_name=_('Контакты'))
    metro = models.ForeignKey(Metros, models.DO_NOTHING, to_field='id', blank=True, null=True, verbose_name=_('Метро'))
    subject = models.ForeignKey(Subjects, models.DO_NOTHING, to_field='id', blank=True, null=True, verbose_name=_('Предмет'))
    city = models.ForeignKey(Cities, models.DO_NOTHING, to_field='id', blank=True, null=True, verbose_name=_('Город'))

    class Meta:
        db_table = 'organizations_vuz'
        unique_together = (('id', 'type', 'source'),)
        verbose_name = _('ВУЗ')
        verbose_name_plural = _('ВУЗы')


class Faculties(models.Model):
    id = models.AutoField(verbose_name=_('ID'), primary_key=True)
    type = models.CharField(verbose_name=_('Тип'), max_length=50)
    source = models.CharField(verbose_name=_('Источник'), max_length=50)
    code = models.IntegerField(verbose_name=_('Код'), blank=True, null=True)
    name = models.CharField(verbose_name=_('Название'), max_length=255)
    post_index = models.CharField(verbose_name=_('Почтовый индекс'), max_length=10, blank=True, null=True)
    address = models.CharField(verbose_name=_('Адрес'), max_length=255, blank=True, null=True)
    email = models.CharField(verbose_name=_('Email'), max_length=100, blank=True, null=True)
    phone = models.CharField(verbose_name=_('Телефон'), max_length=20, blank=True, null=True)
    longitude_latitude = models.CharField(verbose_name=_('Координаты'), max_length=50, blank=True, null=True)
    calculation_data = models.JSONField(verbose_name=_('Расчетные параметры факультета'), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(verbose_name=_('Дата обновления'))
    organization_vuz = models.ForeignKey(OrganizationsVuz, models.DO_NOTHING, to_field='id', blank=True, null=True, verbose_name=_('ВУЗ'))

    class Meta:
        db_table = 'faculties'
        unique_together = (('id', 'type', 'source'),)
        verbose_name = _('Факультет')
        verbose_name_plural = _('Факультеты')


class Forms(models.Model):
    id = models.AutoField(verbose_name=_('ID'), primary_key=True)
    type = models.CharField(verbose_name=_('Тип'), max_length=50)
    source = models.CharField(verbose_name=_('Источник'), max_length=50)
    name = models.CharField(verbose_name=_('Название формы обучения'), max_length=50)
    created_at = models.DateTimeField(verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(verbose_name=_('Дата обновления'))

    class Meta:
        db_table = 'forms'
        unique_together = (('id', 'type', 'source'),)
        verbose_name = _('Форма обучения')
        verbose_name_plural = _('Формы обучения')


class Professions(models.Model):
    id = models.AutoField(verbose_name=_('ID'), primary_key=True)
    type = models.CharField(verbose_name=_('Тип'), max_length=50)
    source = models.CharField(verbose_name=_('Источник'), max_length=50)
    name = models.CharField(verbose_name=_('Название'), max_length=255)
    published = models.BooleanField(verbose_name=_('Опубликовано'))
    code = models.CharField(verbose_name=_('Код'), max_length=50, blank=True, null=True)
    slug = models.CharField(verbose_name=_('Slug'), max_length=255, blank=True, null=True)
    short_text = models.CharField(verbose_name=_('Краткий текст'), max_length=1000, blank=True, null=True)
    full_text = models.CharField(verbose_name=_('Полный текст'), max_length=5000, blank=True, null=True)
    other_text_1 = models.CharField(verbose_name=_('Дополнительный текст 1'), max_length=1000, blank=True, null=True)
    other_text_2 = models.CharField(verbose_name=_('Дополнительный текст 2'), max_length=1000, blank=True, null=True)
    preview_image = models.CharField(verbose_name=_('Превью изображение'), max_length=255, blank=True, null=True)
    detail_image = models.CharField(verbose_name=_('Детальное изображение'), max_length=255, blank=True, null=True)
    organization_type = models.CharField(verbose_name=_('Тип организации'), max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(verbose_name=_('Дата обновления'))
    external_updated_at = models.DateTimeField(verbose_name=_('Дата внешнего обновления'), blank=True, null=True)
    extra_names = models.JSONField(verbose_name=_('Основные формы названия профессии'), blank=True, null=True)

    class Meta:
        db_table = 'professions'
        unique_together = (('id', 'type', 'source'),)
        verbose_name = _('Профессия')
        verbose_name_plural = _('Профессии')


class ProfessionsOrganizations(models.Model):
    profession = models.ForeignKey(Professions, models.DO_NOTHING, to_field='id', verbose_name=_('Профессия'))
    organization_vuz = models.ForeignKey(OrganizationsVuz, models.DO_NOTHING, to_field='id', verbose_name=_('ВУЗ'))

    class Meta:
        db_table = 'professions_organizations'
        unique_together = (('profession', 'organization_vuz'),)
        verbose_name = _('Профессия ВУЗа')
        verbose_name_plural = _('Профессии ВУЗов')


class Specialties(models.Model):
    id = models.AutoField(verbose_name=_('ID'), primary_key=True)
    type = models.CharField(verbose_name=_('Тип'), max_length=50)
    source = models.CharField(verbose_name=_('Источник'), max_length=50)
    name = models.CharField(verbose_name=_('Название'), max_length=500)
    qualification = models.CharField(verbose_name=_('Квалификация'), max_length=255, blank=True, null=True)
    description = models.CharField(verbose_name=_('Описание'), max_length=5000, blank=True, null=True)
    description_work = models.CharField(verbose_name=_('Описание работы'), max_length=5000, blank=True, null=True)
    code = models.CharField(verbose_name=_('Код'), max_length=20, blank=True, null=True)
    code_okso = models.CharField(verbose_name=_('Код ОКСО'), max_length=20, blank=True, null=True)
    code_old = models.CharField(verbose_name=_('Старый код'), max_length=20, blank=True, null=True)
    code_okso_new = models.CharField(verbose_name=_('Новый код ОКСО'), max_length=20, blank=True, null=True)
    level_code = models.CharField(verbose_name=_('Код уровня'), max_length=50, blank=True, null=True)
    calculation_data = models.JSONField(verbose_name=_('Расчетные параметры специальности'), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(verbose_name=_('Дата обновления'))

    class Meta:
        db_table = 'specialties'
        unique_together = (('id', 'type', 'source'),)
        verbose_name = _('Специальность')
        verbose_name_plural = _('Специальности')


class SpecialtiesOrganizations(models.Model):
    specialty = models.ForeignKey(Specialties, models.DO_NOTHING, to_field='id', verbose_name=_('Специальность'))
    organization_vuz = models.ForeignKey(OrganizationsVuz, models.DO_NOTHING, to_field='id', verbose_name=_('ВУЗ'))

    class Meta:
        db_table = 'specialties_organizations'
        unique_together = (('specialty', 'organization_vuz'),)
        verbose_name = _('Специальность ВУЗа')
        verbose_name_plural = _('Специальности ВУЗов')


class Programs(models.Model):
    id = models.AutoField(verbose_name=_('ID'), primary_key=True)
    type = models.CharField(verbose_name=_('Тип'), max_length=50)
    source = models.CharField(verbose_name=_('Источник'), max_length=50)
    profile = models.CharField(verbose_name=_('Название профиля/направления'), max_length=5000, blank=True, null=True)
    duration = models.IntegerField(verbose_name=_('Длительность обучения в месяцах'), blank=True, null=True)
    budget_places = models.IntegerField(verbose_name=_('Количество бюджетных мест'), blank=True, null=True)
    budget_score = models.IntegerField(verbose_name=_('Проходной балл на бюджет'), blank=True, null=True)
    commercial_places = models.IntegerField(verbose_name=_('Количество платных мест'), blank=True, null=True)
    commercial_score = models.IntegerField(verbose_name=_('Проходной балл на платное'), blank=True, null=True)
    cost = models.IntegerField(verbose_name=_('Стоимость обучения'), blank=True, null=True)
    calculation_data = models.JSONField(verbose_name=_('Расчетные данные программы'), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(verbose_name=_('Дата обновления'))
    organization_vuz = models.ForeignKey(OrganizationsVuz, models.DO_NOTHING, to_field='id', blank=True, null=True, verbose_name=_('ВУЗ'))
    faculty = models.ForeignKey(Faculties, models.DO_NOTHING, to_field='id', blank=True, null=True, verbose_name=_('Факультет'))
    specialty = models.ForeignKey(Specialties, models.DO_NOTHING, to_field='id', blank=True, null=True, verbose_name=_('Специальность'))
    form = models.ForeignKey(Forms, models.DO_NOTHING, to_field='id', blank=True, null=True, verbose_name=_('Форма обучения'))

    class Meta:
        db_table = 'programs'
        unique_together = (('id', 'type', 'source'),)
        verbose_name = _('Программа')
        verbose_name_plural = _('Программы')
