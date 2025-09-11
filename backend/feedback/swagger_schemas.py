from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


order_schema = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            'ordering', openapi.IN_QUERY,
            description="Поле для сортировки. Пример: 'total_feedbacks' или '-total_feedbacks'. \
                Также есть возможность сортировки по рейтингу: 'total_rating' или '-total_rating'.",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'title', openapi.IN_QUERY,
            description="Строка для поиска по 'title' у автора. Пример: 'высокий' или 'Иван'.",
            type=openapi.TYPE_STRING
        )
    ],
    operation_description="Получить список авторов, отсортированных по отзывам и рейтингу, \
        с возможностью поиска по названию."
)

top_filters_count_schema = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            'top', openapi.IN_QUERY,
            description="Фильтр по категории верхнего уровня. Пример: 'master', 'language', 'school', 'offline', 'online', 'university', 'training'.",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'learning_types', openapi.IN_QUERY,
            description="Фильтр по типам обучения. Можно указать несколько значений через запятую.",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'course_formats', openapi.IN_QUERY,
            description="Фильтр по форматам курсов. Можно указать несколько значений через запятую.",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'courses_thematics', openapi.IN_QUERY,
            description="Фильтр по тематикам курсов. Можно указать несколько значений через запятую.",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'course_levels', openapi.IN_QUERY,
            description="Фильтр по уровням курсов. Можно указать несколько значений через запятую.",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'price_min', openapi.IN_QUERY,
            description="Минимальная цена курса.",
            type=openapi.TYPE_NUMBER
        ),
        openapi.Parameter(
            'price_max', openapi.IN_QUERY,
            description="Максимальная цена курса.",
            type=openapi.TYPE_NUMBER
        ),
        openapi.Parameter(
            'organization', openapi.IN_QUERY,
            description="Название организации (поиск по подстроке).",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'author_types', openapi.IN_QUERY,
            description="Тип автора курса.",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'minimal_rating', openapi.IN_QUERY,
            description="Минимальный рейтинг курса (от 1 до 5).",
            type=openapi.TYPE_NUMBER
        )
    ],
    operation_description="Получить количество авторов курсов по категориям с возможностью фильтрации. Результаты группируются по различным категориям курсов."
)
