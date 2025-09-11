from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


statistics_schema = swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date', 
                openapi.IN_QUERY, 
                description="Start date for the statistics (format: YYYY-MM-DD)", 
                type=openapi.TYPE_STRING, 
                required=False
            ),
            openapi.Parameter(
                'end_date', 
                openapi.IN_QUERY, 
                description="End date for the statistics (format: YYYY-MM-DD)", 
                type=openapi.TYPE_STRING, 
                required=False
            ),
        ]
    )