from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


program_filter_schema = swagger_auto_schema(
        operation_description="Получение списка программ для указанного ВУЗа с возможностью фильтрации",
        operation_summary="Список программ ВУЗа",
        manual_parameters=[
            openapi.Parameter(
                'name', 
                openapi.IN_QUERY, 
                description='Фильтр по названию программы (поддерживает частичное совпадение)', 
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'faculty', 
                openapi.IN_QUERY, 
                description='Фильтр по названию факультета', 
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'specialty', 
                openapi.IN_QUERY, 
                description='Фильтр по названию специальности', 
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'form', 
                openapi.IN_QUERY, 
                description='Фильтр по названию формы обучения (Очно/Заочно/Очно-заочно/Дистанционно)', 
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'budget_places_min', 
                openapi.IN_QUERY, 
                description='Минимальное количество бюджетных мест', 
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'budget_places_max', 
                openapi.IN_QUERY, 
                description='Максимальное количество бюджетных мест', 
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'min_budget_score', 
                openapi.IN_QUERY, 
                description='Минимальный проходной балл на бюджет', 
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'max_budget_score', 
                openapi.IN_QUERY, 
                description='Максимальный проходной балл на бюджет', 
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'min_commercial_places', 
                openapi.IN_QUERY, 
                description='Минимальное количество платных мест', 
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'max_commercial_places', 
                openapi.IN_QUERY, 
                description='Максимальное количество платных мест', 
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'min_commercial_score', 
                openapi.IN_QUERY, 
                description='Минимальный проходной балл на платное обучение', 
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'max_commercial_score', 
                openapi.IN_QUERY, 
                description='Максимальный проходной балл на платное обучение', 
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'price_min', 
                openapi.IN_QUERY, 
                description='Минимальная стоимость обучения', 
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'price_max', 
                openapi.IN_QUERY, 
                description='Максимальная стоимость обучения', 
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'min_duration', 
                openapi.IN_QUERY, 
                description='Минимальная продолжительность обучения (в месяцах)', 
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'max_duration', 
                openapi.IN_QUERY, 
                description='Максимальная продолжительность обучения (в месяцах)', 
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'ordering', 
                openapi.IN_QUERY, 
                description='Поля для сортировки программ. Используйте "-" перед полем для сортировки по убыванию. Доступные поля: cost, budget_score, commercial_score, specialty (сортировка по уровню образования). Пример: "-cost" - сортировка по убыванию стоимости, "specialty" - сортировка по возрастанию уровня образования', 
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'limit', 
                openapi.IN_QUERY, 
                description='Максимальное количество программ в ответе (по умолчанию 10, максимум 100)', 
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'offset', 
                openapi.IN_QUERY, 
                description='Смещение от начала списка программ (для пагинации)', 
                type=openapi.TYPE_INTEGER
            ),
        ]
    )

vuz_filters_schema = swagger_auto_schema(
    operation_description="Получение доступных значений фильтров для ВУЗов на основе текущего выбора. Запрос оптимизирован для быстрой работы с большими наборами данных.",
    operation_summary="Фильтры для ВУЗов",
    manual_parameters=[
        openapi.Parameter(
            'filter_type',
            openapi.IN_QUERY,
            description="Тип фильтра (city/subject/metro/faculty/specialty/form/level_code/organization_type)",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'limit',
            openapi.IN_QUERY,
            description="Количество элементов на странице",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'offset',
            openapi.IN_QUERY,
            description="Смещение от начала списка",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Поисковый запрос для фильтрации значений в выбранном типе фильтра",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'cities',
            openapi.IN_QUERY,
            description="Список ID городов через запятую для приоритетной сортировки",
            type=openapi.TYPE_STRING
        )
    ],
    responses={
        200: 'VuzFiltersSerializer',
        400: 'Неверные параметры запроса'
    }
)

program_filters_schema = swagger_auto_schema(
    operation_description="Получение доступных значений фильтров для программ обучения на основе текущего выбора",
    operation_summary="Фильтры для программ обучения",
    manual_parameters=[
        openapi.Parameter(
            'name', 
            openapi.IN_QUERY, 
            description='Фильтр по названию программы (поддерживает частичное совпадение)', 
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'faculty', 
            openapi.IN_QUERY, 
            description='Фильтр по названию факультета', 
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'specialty', 
            openapi.IN_QUERY, 
            description='Фильтр по названию специальности', 
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'form', 
            openapi.IN_QUERY, 
            description='Фильтр по названию формы обучения (Очно/Заочно/Очно-заочно/Дистанционно)', 
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'min_budget_places', 
            openapi.IN_QUERY, 
            description='Минимальное количество бюджетных мест', 
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'max_budget_places', 
            openapi.IN_QUERY, 
            description='Максимальное количество бюджетных мест', 
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'min_budget_score', 
            openapi.IN_QUERY, 
            description='Минимальный проходной балл на бюджет', 
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'max_budget_score', 
            openapi.IN_QUERY, 
            description='Максимальный проходной балл на бюджет', 
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'min_commercial_places', 
            openapi.IN_QUERY, 
            description='Минимальное количество платных мест', 
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'max_commercial_places', 
            openapi.IN_QUERY, 
            description='Максимальное количество платных мест', 
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'min_commercial_score', 
            openapi.IN_QUERY, 
            description='Минимальный проходной балл на платное обучение', 
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'max_commercial_score', 
            openapi.IN_QUERY, 
            description='Максимальный проходной балл на платное обучение', 
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'price_min', 
            openapi.IN_QUERY, 
            description='Минимальная стоимость обучения', 
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'price_max', 
            openapi.IN_QUERY, 
            description='Максимальная стоимость обучения', 
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'duration_min', 
            openapi.IN_QUERY, 
            description='Минимальная продолжительность обучения (в месяцах)', 
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'duration_max', 
            openapi.IN_QUERY, 
            description='Максимальная продолжительность обучения (в месяцах)', 
            type=openapi.TYPE_INTEGER
        ),
    ],
    responses={
        200: 'ProgramFiltersSerializer',
        400: 'Неверные параметры запроса'
    }
)
