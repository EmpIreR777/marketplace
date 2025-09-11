from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from author.utils import profile_document_path, logos_document_path

User = get_user_model()


class AuthorType(models.TextChoices):
    INDIVIDUAL = 'INDIVIDUAL', _('Физическое лицо')
    INDIVIDUAL_ENTREPRENEUR = 'INDIVIDUAL_ENTREPRENEUR', _('Индивидуальный предприниматель')
    ORGANIZATION = 'ORGANIZATION', _('Организация')


class VerificationProfileType(models.TextChoices):
    UNVERIFIED = 'UNVERIFIED', _('Не проверен')
    ON_VERIFICATION = 'ON_VERIFICATION', _('На проверке')
    VERIFIED = 'VERIFIED', _('Проверен')


class DocumentType(models.Model):
    document_type = models.CharField(
        verbose_name=_('Документ'),
        max_length=150,
        unique=True,
    )

    class Meta:
        verbose_name = _('Тип Документа')
        verbose_name_plural = _('Типы Документов')

    def __str__(self):
        return self.document_type if self.document_type else f'DocumentType({self.id})'


class RequiredDocument(models.Model):
    author_type = models.CharField(
        verbose_name=_('Тип автора'),
        max_length=150,
        choices=AuthorType.choices,
        default=AuthorType.INDIVIDUAL,
    )
    document_types = models.ManyToManyField(
        verbose_name=_('Типы документов'),
        to=DocumentType
    )

    class Meta:
        verbose_name = _('Обязательные Документ')
        verbose_name_plural = _('Обязательные Документы')

    def __str__(self):
        return f'Обязательные документы для {AuthorType(self.author_type).label}'


class Document(models.Model):
    author = models.ForeignKey(
        verbose_name=_('Автор'),
        to='author.Author',
        on_delete=models.CASCADE,
        related_name='documents',
    )
    document_type = models.ForeignKey(
        verbose_name=_('Тип документа'),
        to=DocumentType,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    file = models.FileField(
        verbose_name=_('Документ'),
        upload_to=profile_document_path,
    )

    class Meta:
        verbose_name = _('Документ')
        verbose_name_plural = _('Документы')

    def __str__(self):
        return f'Документы для автора {self.author}'


class Author(User):
    author_type = models.CharField(
        verbose_name=_('Тип автора'),
        max_length=150,
        choices=AuthorType.choices,
        default=AuthorType.INDIVIDUAL,
    )
    title = models.CharField(
        verbose_name=_('Название'),
        max_length=255,
        help_text=_('Название организации автора'),
    )
    full_title = models.CharField(
        verbose_name=_('Полное название'),
        max_length=1000,
        blank=True,
        null=True,
    )
    alias = models.CharField(
        verbose_name=_('Короткое название'),
        max_length=1000,
        blank=True,
        null=True,
    )
    prepositional_title = models.CharField(
        verbose_name=_('Название в предложном падеже'),
        max_length=1000,
        blank=True,
        null=True,
    )
    genitive_title = models.CharField(
        verbose_name=_('Название в родительском падеже'),
        max_length=1000,
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name=_('Описание'),
        blank=True,
        null=True,
    )
    logo = models.ImageField(
        verbose_name=_('Логотип'),
        upload_to=logos_document_path,
        blank=True,
        null=True,
    )
    website = models.URLField(
        verbose_name=_('Веб-сайт'),
        blank=True,
        null=True,
    )
    address = models.CharField(
        verbose_name=_('Адрес'),
        max_length=1000,
        blank=True,
        null=True,
    )
    legal_address = models.CharField(
        verbose_name=_('Адрес регистрации'),
        max_length=1000,
        blank=True,
        null=True,
    )
    education_type = models.CharField(
        verbose_name=_('Тип образования'),
        max_length=255,
        blank=True,
        null=True,
    )
    is_premium_partner = models.BooleanField(
        verbose_name=_('Премиум партнёр?'),
        default=False,
    )
    verification_status = models.CharField(
        verbose_name=_('Статус проверки'),
        max_length=150,
        choices=VerificationProfileType.choices,
        default=VerificationProfileType.UNVERIFIED,
    )
    is_verified = models.BooleanField(_('Верифицирован автор?'), default=False,)

    class Meta:
        verbose_name = _('Автор')
        verbose_name_plural = _('Авторы')
        
    def save(self, *args, **kwargs):
        self.is_verified = self.verification_status == VerificationProfileType.VERIFIED
        super().save(*args, **kwargs)
        

    def __str__(self):
        return self.title if self.title else f'Author({self.id})'


class FIZAuthor(models.Model):
    author = models.OneToOneField(
        verbose_name=_('Автор'),
        to=Author,
        on_delete=models.CASCADE,
        related_name='fiz_author'
    )
    fio = models.CharField(
        verbose_name=_('ФИО'),
        max_length=255,
        blank=True,
        null=True
    )
    fio_short = models.CharField(
        verbose_name=_('Краткое ФИО'),
        max_length=255,
        blank=True,
        null=True
    )
    email = models.EmailField(
        verbose_name=_('Рабочая электронная почта'),
        blank=True,
        null=True
    )
    passport_serial = models.CharField(
        verbose_name=_('Серия паспорта'),
        max_length=100,
        blank=True,
        null=True
    )
    passport_number = models.CharField(
        verbose_name=_('Номер паспорта'),
        max_length=100,
        blank=True,
        null=True
    )
    passport_date = models.DateField(
        verbose_name=_('Дата выдачи паспорта'),
        blank=True,
        null=True,
    )
    passport_issued_by = models.CharField(
        verbose_name=_('Кем выдан паспорт'),
        max_length=255,
        blank=True,
        null=True
    )
    passport_code_department = models.CharField(
        verbose_name=_('Код подразделения'),
        max_length=100,
        blank=True,
        null=True
    )
    inn = models.CharField(
        verbose_name=_('ИНН'),
        max_length=100,
        blank=True,
        null=True
    )
    contact_number = models.CharField(
        verbose_name=_('Контактный телефон'),
        max_length=100,
        blank=True,
        null=True
    )
    address = models.CharField(
        verbose_name=_('Адрес'),
        max_length=1000,
        blank=True,
        null=True
    )
    snils = models.CharField(
        verbose_name=_('СНИЛС'),
        max_length=100,
        blank=True,
        null=True
    )
    bank_name = models.CharField(
        verbose_name=_('Название банка'),
        max_length=255,
        blank=True,
        null=True
    )
    bank_bik = models.CharField(
        verbose_name=_('БИК банка'),
        max_length=100,
        blank=True,
        null=True
    )
    bank_ks = models.CharField(
        verbose_name=_('КС банка'),
        max_length=100,
        blank=True,
        null=True
    )
    bank_rs = models.CharField(
        verbose_name=_('РС банка'),
        max_length=100,
        blank=True,
        null=True
    )

    
class FOPAuthor(models.Model):
    author = models.OneToOneField(
        verbose_name=_('Автор'),
        to=Author,
        on_delete=models.CASCADE,
        related_name='fop_author'
    )
    fio = models.CharField(
        verbose_name=_('ФИО'),
        max_length=255,
        blank=True,
        null=True
    )
    fio_short = models.CharField(
        verbose_name=_('Краткое ФИО'),
        max_length=255,
        blank=True,
        null=True
    )
    email = models.EmailField(
        verbose_name=_('Рабочая электронная почта'),
        blank=True,
        null=True
    )
    reg_number = models.CharField(
        verbose_name=_('Регистрационный номер в реестре'),
        max_length=100,
        blank=True,
        null=True
    )
    reg_date = models.DateField(
        verbose_name=_('Дата регистрации'),
        blank=True,
        null=True
    )
    address = models.CharField(
        verbose_name=_('Адрес'),
        max_length=1000,
        blank=True,
        null=True
    )
    contact_number = models.CharField(
        verbose_name=_('Контактный телефон'),
        max_length=100,
        blank=True,
        null=True
    )
    inn = models.CharField(
        verbose_name=_('ИНН'),
        max_length=100,
        blank=True,
        null=True
    )
    bank_name = models.CharField(
        verbose_name=_('Название банка'),
        max_length=255,
        blank=True,
        null=True
    )
    bank_bik = models.CharField(
        verbose_name=_('БИК банка'),
        max_length=100,
        blank=True,
        null=True
    )
    bank_ks = models.CharField(
        verbose_name=_('КС банка'),
        max_length=100,
        blank=True,
        null=True
    )
    bank_rs = models.CharField(
        verbose_name=_('РС банка'),
        max_length=100,
        blank=True,
        null=True
    )
    ogrnip_number = models.CharField(
        verbose_name=_('ОГРНИП'),
        max_length=100,
        blank=True,
        null=True
    )


class LLCAuthor(models.Model):
    author = models.OneToOneField(
        verbose_name=_('Автор'),
        to=Author,
        on_delete=models.CASCADE,
        related_name='llc_author'
    )
    email = models.EmailField(
        verbose_name=_('Электронная почта организации'),
        blank=True,
        null=True
    )
    name = models.CharField(
        verbose_name=_('Название организации'),
        max_length=255,
        blank=True,
        null=True
    )
    name_short = models.CharField(
        verbose_name=_('Краткое название организации'),
        max_length=255,
        blank=True,
        null=True
    )
    director_name = models.CharField(
        verbose_name=_('Имя директора'),
        max_length=255,
        blank=True,
        null=True
    )
    director_short_name = models.CharField(
        verbose_name=_('Сокращенное имя директора'),
        max_length=255,
        blank=True,
        null=True
    )
    buhgaler_name = models.CharField(
        verbose_name=_('Имя бухгалтера'),
        max_length=255,
        blank=True,
        null=True
    )
    buhgaler_short_name = models.CharField(
        verbose_name=_('Сокращенное имя бухгалтера'),
        max_length=255,
        blank=True,
        null=True
    )
    kpp = models.CharField(
        verbose_name=_('КПП'),
        max_length=100,
        blank=True,
        null=True
    )
    okpo = models.CharField(
        verbose_name=_('ОКПО'),
        max_length=100,
        blank=True,
        null=True
    )
    registration_date = models.DateField(
        verbose_name=_('Дата регистрации'),
        blank=True,
        null=True
    )
    oktmo = models.CharField(
        verbose_name=_('ОКТМО'),
        max_length=100,
        blank=True,
        null=True
    )
    ogrn = models.CharField(
        verbose_name=_('ОГРН'),
        max_length=100,
        blank=True,
        null=True
    )
    inn = models.CharField(
        verbose_name=_('ИНН'),
        max_length=100,
        blank=True,
        null=True
    )
    contact_number = models.CharField(
        verbose_name=_('Контактный телефон'),
        max_length=100,
        blank=True,
        null=True
    )
    bank_name = models.CharField(
        verbose_name=_('Название банка'),
        max_length=255,
        blank=True,
        null=True
    )
    bank_bik = models.CharField(
        verbose_name=_('БИК банка'),
        max_length=100,
        blank=True,
        null=True
    )
    bank_ks = models.CharField(
        verbose_name=_('КС банка'),
        max_length=100,
        blank=True,
        null=True
    )
    bank_rs = models.CharField(
        verbose_name=_('РС банка'),
        max_length=100,
        blank=True,
        null=True
    )
    