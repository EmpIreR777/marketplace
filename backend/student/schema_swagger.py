from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from student.serializers import StudentScheduleSerializer

student_schedule_schema = swagger_auto_schema(
    operation_description="Получить курсы в промежутке недели, месяца, года",
    manual_parameters=[
        openapi.Parameter(
            'filter',
            openapi.IN_QUERY,
            description="Период для фильтра: неделя, месяц, год",
            type=openapi.TYPE_STRING,
            enum=['week', 'month', 'year'],
        )
    ],
    responses={
        200: openapi.Response(
            description="Расписание",
            schema=StudentScheduleSerializer(many=True)
        ),
        400: "Неверные параметры",
        404: "Студент или курс не найдены"
    }
)

student_bought_courses_schema = swagger_auto_schema(
    operation_description="Get student's purchased courses with optional filtering and sorting",
    manual_parameters=[
        openapi.Parameter(
            'ordering', openapi.IN_QUERY, description="Ordering of the results",
            type=openapi.TYPE_STRING, enum=['-purchase_date', 'purchase_date']
        ),
        openapi.Parameter(
            'learning_types', openapi.IN_QUERY, description="ID типов обучения",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'course_levels', openapi.IN_QUERY, description="ID уровней курсов",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'course_formats', openapi.IN_QUERY, description="ID форматов курсов",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'courses_thematics', openapi.IN_QUERY, description="ID тематик курсов",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'age_category', openapi.IN_QUERY, description="ID возрастных категорий",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'has_job_help', openapi.IN_QUERY, description="Фильтр по наличию помощи с трудоустройством",
            type=openapi.TYPE_BOOLEAN
        ),
        openapi.Parameter(
            'has_job_guarantee', openapi.IN_QUERY, description="Фильтр по гарантии трудоустройства",
            type=openapi.TYPE_BOOLEAN
        ),
        openapi.Parameter(
            'provides_diploma', openapi.IN_QUERY, description="Фильтр по выдаче диплома",
            type=openapi.TYPE_BOOLEAN
        ),
        openapi.Parameter(
            'has_mentor', openapi.IN_QUERY, description="Фильтр по наличию наставника",
            type=openapi.TYPE_BOOLEAN
        ),
        openapi.Parameter(
            'is_webinar', openapi.IN_QUERY, description="Фильтр по вебинарам",
            type=openapi.TYPE_BOOLEAN
        ),
        openapi.Parameter(
            'is_top_sale', openapi.IN_QUERY, description="Фильтр по топ-продажам",
            type=openapi.TYPE_BOOLEAN
        ),
    ]
)
