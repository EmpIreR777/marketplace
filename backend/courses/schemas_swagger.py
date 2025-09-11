from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from courses.filters_serializers import CourseTypesSerializer
from courses.serializers import CourseOutSerializer, CourseBaseSerializer, CourseCreateSerializer, CourseListSerializer


unmoderated_courses_schema = swagger_auto_schema(
    methods=['get'],
    operation_summary="Получить немодерированные курсы",
    operation_description="Возвращает список курсов, которые еще не прошли модерацию. \
                           Доступно только администраторам.",
    manual_parameters=[
        openapi.Parameter(
            name="page",
            in_=openapi.IN_QUERY,
            description="Номер страницы для пагинации",
            type=openapi.TYPE_INTEGER,
            required=False,
        ),
        openapi.Parameter(
            name="page_size",
            in_=openapi.IN_QUERY,
            description="Количество элементов на странице",
            type=openapi.TYPE_INTEGER,
            required=False,
        ),
    ],
    responses={
        200: openapi.Response(
            description="Список немодерированных курсов",
            schema=CourseOutSerializer(many=True),
        ),
        403: openapi.Response(
            description="Доступ запрещен",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING)
                },
            ),
        ),
    },
)


my_courses_schema = swagger_auto_schema(
    methods=['get'],
    operation_summary="Получить список курсов пользователя",
    operation_description="Возвращает список курсов, у которых \
                           аутентифицированный пользователь является автором.",
    manual_parameters=[
        openapi.Parameter(
            name="page",
            in_=openapi.IN_QUERY,
            description="Номер страницы для пагинации",
            type=openapi.TYPE_INTEGER,
            required=False,
        ),
        openapi.Parameter(
            name="page_size",
            in_=openapi.IN_QUERY,
            description="Количество элементов на странице",
            type=openapi.TYPE_INTEGER,
            required=False,
        ),
    ],
    responses={
        200: openapi.Response(
            description="Список курсов пользователя",
            schema=CourseOutSerializer(many=True),
        ),
        401: openapi.Response(
            description="Пользователь не аутентифицирован",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING)
                },
            ),
        ),
    },
)

my_courses_update_schema = swagger_auto_schema(
    methods=['patch'],
    operation_summary="Обновить курс пользователя",
    operation_description="Позволяет пользователю обновить информацию о курсе, если он является автором этого курса.",
    manual_parameters=[
        openapi.Parameter(
            name="id",
            in_=openapi.IN_PATH,
            description="ID курса, который нужно обновить",
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ],
    request_body=CourseCreateSerializer,
    responses={
        200: openapi.Response(
            description="Данные обновленного курса",
            schema=CourseCreateSerializer(),
        ),
        400: openapi.Response(
            description="Ошибка валидации данных",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING)
                },
            ),
        ),
        404: openapi.Response(
            description="Курс не найден или у пользователя нет прав на его редактирование",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING)
                },
            ),
        ),
        401: openapi.Response(
            description="Пользователь не аутентифицирован",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING)
                },
            ),
        ),
    },
)

moderate_course_schema = swagger_auto_schema(
    method='patch',
    operation_summary="Модерировать курс",
    operation_description="Позволяет администратору модерировать конкретный курс.",
    manual_parameters=[
        openapi.Parameter(
            name="id",
            in_=openapi.IN_PATH,
            description="ID курса, который нужно модерировать",
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ],
    request_body=CourseBaseSerializer,
    responses={
        200: openapi.Response(
            description="Обновленные данные курса",
            schema=CourseBaseSerializer(),
        ),
        400: openapi.Response(
            description="Ошибка валидации",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING)
                },
            ),
        ),
        404: openapi.Response(
            description="Курс не найден",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING)
                },
            ),
        ),
    },
)
similar_courses_schema = swagger_auto_schema(
    method='get',
    operation_summary="Получить похожие курсы",
    operation_description="Позволяет передать ID курса и получить 5 похожих на него по различным тематикам,"
                          " или топ 5 если курс не найден",
)

filters_for_courses_schema = swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'top',
                openapi.IN_QUERY,
                description="Фильтр по основным категориям (school - Школы, master - Мастер-классы, "
                          "language - Языковые курсы, offline - Оффлайн курсы, "
                          "university - ВУЗы, training - Тренинги)",
                type=openapi.TYPE_STRING,
                example="school"
            ),
            openapi.Parameter(
                'learning_types',
                openapi.IN_QUERY,
                description="Типы обучения (можно указать несколько через запятую или повторить параметр)",
                type=openapi.TYPE_STRING,
                example="typeProgramming,typeAnalytics"
            ),
            openapi.Parameter(
                'courses_thematics',
                openapi.IN_QUERY,
                description="Специализации (можно указать несколько через запятую или повторить параметр)",
                type=openapi.TYPE_STRING,
                example="webDev,mobileDev"
            ),
            openapi.Parameter(
                'course_targets',
                openapi.IN_QUERY,
                description="Цели курса (можно указать несколько через запятую или повторить параметр)",
                type=openapi.TYPE_STRING,
                example="upgradeSkills,changeJob"
            ),
            openapi.Parameter(
                'course_formats',
                openapi.IN_QUERY,
                description="Форматы обучения (можно указать несколько через запятую или повторить параметр)",
                type=openapi.TYPE_STRING,
                example="online,offline"
            ),
            openapi.Parameter(
                'course_levels',
                openapi.IN_QUERY,
                description="Уровни программы (можно указать несколько через запятую или повторить параметр)",
                type=openapi.TYPE_STRING,
                example="beginner,intermediate"
            ),
            openapi.Parameter(
                'author_type',
                openapi.IN_QUERY,
                description="Типы авторов(INDIVIDUAL_ENTREPRENEUR, INDIVIDUAL, ORGANIZATION)",
                type=openapi.TYPE_STRING,
                example="INDIVIDUAL_ENTREPRENEUR, INDIVIDUAL, ORGANIZATION"
            ),
            openapi.Parameter(
                'price_min',
                openapi.IN_QUERY,
                description="Минимальная цена",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'price_max',
                openapi.IN_QUERY,
                description="Максимальная цена",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'duration_min',
                openapi.IN_QUERY,
                description="Минимальная длительность (месяцев)",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'duration_max',
                openapi.IN_QUERY,
                description="Максимальная длительность (месяцев)",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: CourseTypesSerializer,
            400: 'Неверные параметры запроса'
        },
        operation_description="""
        Получение доступных значений фильтров на основе текущего выбора.
        
        Все фильтры с множественным выбором поддерживают два формата:
        1. Через запятую: ?learning_types=typeProgramming,typeAnalytics
        2. Через повторение параметра: ?learning_types=typeProgramming&learning_types=typeAnalytics
        
        Возвращает только те значения фильтров, которые доступны для текущего выбора.
        """
    )

course_list_schema = swagger_auto_schema(
    operation_summary="Получить список курсов",
    operation_description="Возвращает список всех активных и модерированных курсов с возможностью фильтрации",
    manual_parameters=[
        openapi.Parameter(
            'top',
            openapi.IN_QUERY,
            description="Фильтр по основным категориям (school - Школы, master - Мастер-классы, "
                      "language - Языковые курсы, offline - Оффлайн курсы, online - Онлайн курсы, "
                      "university - ВУЗы, training - Тренинги)",
            type=openapi.TYPE_STRING,
            example="school"
        ),
        openapi.Parameter(
            'price_min',
            openapi.IN_QUERY,
            description="Минимальная цена",
            type=openapi.TYPE_NUMBER
        ),
        openapi.Parameter(
            'price_max',
            openapi.IN_QUERY,
            description="Максимальная цена",
            type=openapi.TYPE_NUMBER
        ),
        openapi.Parameter(
            'ordering',
            openapi.IN_QUERY,
            description="Сортировка (name, -name, price, -price, organization, -organization, date_start, -date_start)",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'author_id',
            openapi.IN_QUERY,
            description="ID автора курса",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'author_types',
            openapi.IN_QUERY,
            description="Типы авторов(INDIVIDUAL_ENTREPRENEUR, INDIVIDUAL, ORGANIZATION)",
            type=openapi.TYPE_STRING,
            example="INDIVIDUAL_ENTREPRENEUR, INDIVIDUAL, ORGANIZATION"
        ),
    ],
    responses={
        200: openapi.Response(
            description="Список курсов",
            schema=CourseListSerializer(many=True)
        )
    }
)



author_courses_filters_schema = swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'learning_types',
                openapi.IN_QUERY,
                description="Типы обучения (можно указать несколько через запятую или повторить параметр)",
                type=openapi.TYPE_STRING,
                example="typeProgramming,typeAnalytics"
            ),
            openapi.Parameter(
                'courses_thematics',
                openapi.IN_QUERY,
                description="Специализации (можно указать несколько через запятую или повторить параметр)",
                type=openapi.TYPE_STRING,
                example="webDev,mobileDev"
            ),
            openapi.Parameter(
                'course_targets',
                openapi.IN_QUERY,
                description="Цели курса (можно указать несколько через запятую или повторить параметр)",
                type=openapi.TYPE_STRING,
                example="upgradeSkills,changeJob"
            ),
            openapi.Parameter(
                'course_formats',
                openapi.IN_QUERY,
                description="Форматы обучения (можно указать несколько через запятую или повторить параметр)",
                type=openapi.TYPE_STRING,
                example="online,offline"
            ),
            openapi.Parameter(
                'course_levels',
                openapi.IN_QUERY,
                description="Уровни программы (можно указать несколько через запятую или повторить параметр)",
                type=openapi.TYPE_STRING,
                example="beginner,intermediate"
            ),
            openapi.Parameter(
                'price_min',
                openapi.IN_QUERY,
                description="Минимальная цена",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'price_max',
                openapi.IN_QUERY,
                description="Максимальная цена",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'duration_min',
                openapi.IN_QUERY,
                description="Минимальная длительность (месяцев)",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'duration_max',
                openapi.IN_QUERY,
                description="Максимальная длительность (месяцев)",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: CourseTypesSerializer,
            400: 'Неверные параметры запроса'
        },
        operation_description="""
        Получение доступных значений фильтров на основе текущего выбора.
        
        Все фильтры с множественным выбором поддерживают два формата:
        1. Через запятую: ?learning_types=typeProgramming,typeAnalytics
        2. Через повторение параметра: ?learning_types=typeProgramming&learning_types=typeAnalytics
        
        Возвращает только те значения фильтров, которые доступны для текущего выбора.
        """
    )

top_filters_count_schema = swagger_auto_schema(
    method='get',
    operation_summary="Получить количество курсов по категориям с учетом фильтров",
    operation_description="Возвращает количество курсов по основным категориям с учетом примененных фильтров. "
                        "Позволяет узнать, сколько курсов будет в каждой категории после применения фильтров.",
    manual_parameters=[
        openapi.Parameter(
            'learning_types',
            openapi.IN_QUERY,
            description="Типы обучения (можно указать несколько через запятую или повторить параметр)",
            type=openapi.TYPE_STRING,
            example="typeProgramming,typeAnalytics"
        ),
        openapi.Parameter(
            'courses_thematics',
            openapi.IN_QUERY,
            description="Специализации (можно указать несколько через запятую или повторить параметр)",
            type=openapi.TYPE_STRING,
            example="webDev,mobileDev"
        ),
        openapi.Parameter(
            'course_targets',
            openapi.IN_QUERY,
            description="Цели курса (можно указать несколько через запятую или повторить параметр)",
            type=openapi.TYPE_STRING,
            example="upgradeSkills,changeJob"
        ),
        openapi.Parameter(
            'course_formats',
            openapi.IN_QUERY,
            description="Форматы обучения (можно указать несколько через запятую или повторить параметр)",
            type=openapi.TYPE_STRING,
            example="online,offline"
        ),
        openapi.Parameter(
            'course_levels',
            openapi.IN_QUERY,
            description="Уровни программы (можно указать несколько через запятую или повторить параметр)",
            type=openapi.TYPE_STRING,
            example="beginner,intermediate"
        ),
        openapi.Parameter(
            'author_type',
            openapi.IN_QUERY,
            description="Типы авторов(INDIVIDUAL_ENTREPRENEUR, INDIVIDUAL, ORGANIZATION)",
            type=openapi.TYPE_STRING,
            example="INDIVIDUAL_ENTREPRENEUR, INDIVIDUAL, ORGANIZATION"
        ),
        openapi.Parameter(
            'price_min',
            openapi.IN_QUERY,
            description="Минимальная цена",
            type=openapi.TYPE_NUMBER
        ),
        openapi.Parameter(
            'price_max',
            openapi.IN_QUERY,
            description="Максимальная цена",
            type=openapi.TYPE_NUMBER
        ),
        openapi.Parameter(
            'duration_min',
            openapi.IN_QUERY,
            description="Минимальная длительность (месяцев)",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'duration_max',
            openapi.IN_QUERY,
            description="Максимальная длительность (месяцев)",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Поиск по названию курса",
            type=openapi.TYPE_STRING
        ),
    ],
    responses={
        200: openapi.Response(
            description="Количество курсов по категориям",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'master': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'language': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'offline': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'online': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'university': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'training': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'school': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'total_filtered_courses': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'total_courses': openapi.Schema(type=openapi.TYPE_INTEGER),
                }
            )
        )
    }
)