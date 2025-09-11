from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from author.views import AuthorView
from courses.views import CourseErrorMarkReadView, CourseViewSet, FiltersForCoursesView, CourseErrorView, \
    MainPageStatistic, MyCoursesFiltersView, ThematicsTypesView
from maintenance.schema_generator import BothHttpAndHttpsSchemaGenerator
from feedback.views import FeedbackViewSet, AuthorTopByFeedbacksViewSet, FiltersForAuthorsView, FeedbackTopFiltersCountView
from notification.views import NotificationViewSet
from questions.views import QuestionViewSet, QuizView
from organizations.views import OrganizationViewSet
from student.views import StudentViewSet
from tariffs.views import TariffViewSet
from userauth.views import UserViewSet
from contacts.views import ContactsView
from vuz.views import OrganizationVuzViewSet, ProgramViewSet, FiltersForVuzView, FiltersForProgramsView

router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet, basename='organizations')
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'feedbacks', FeedbackViewSet, basename='feedbacks')
router.register(r'author-top-by-feedbacks', AuthorTopByFeedbacksViewSet, basename='author-top')
router.register(r'author', AuthorView, basename="author")
router.register(r'auth/users', UserViewSet, basename="auth")
router.register("notifications", NotificationViewSet, basename="notifications")
router.register(r'tariffs', TariffViewSet, basename='tariffs')
router.register(r'student', StudentViewSet, basename='student')
router.register(r'vuz', OrganizationVuzViewSet, basename='vuz')


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Документация API для course-market",
        contact=openapi.Contact(email="support@yourwebsite.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    generator_class=BothHttpAndHttpsSchemaGenerator,
    permission_classes=(AllowAny,),
)

urlpatterns = ([
    path('admin/', admin.site.urls),
    path('api/', include([
        path('main_page_statistic/', MainPageStatistic.as_view(), name='main-page-statistic'),
        path('courses/my_courses/', CourseViewSet.as_view({'get': 'my_courses'}), name='my-courses'),
        path('courses/error/<uuid:course_id>/', CourseErrorView.as_view(), name='course-error'),
        path('courses/error/<uuid:course_id>/read/', CourseErrorMarkReadView.as_view(), name='course-error-read'),
        path('contacts/', ContactsView.as_view(), name='contacts'),
        path('vuz/<int:vuz_id>/programs/', ProgramViewSet.as_view({'get': 'list'}), name='vuz-programs-list'),
        path('vuz-filters/', FiltersForVuzView.as_view(), name='vuz-filters'),
        path('vuz/<int:vuz_id>/programs/filters/', FiltersForProgramsView.as_view(), name='program-filters'),
        path('', include(router.urls)),
        path('', include('payments.urls')),
        path("questions/", QuestionViewSet.as_view({"get": "list"}), name="questions"),
        path('quiz/', QuizView.as_view(), name='quiz'),
        path('courses-filters/', FiltersForCoursesView.as_view()),
        path('my-courses-filters/', MyCoursesFiltersView.as_view()),
        path('thematics-types/', ThematicsTypesView.as_view()),
        path('author-filters/', FiltersForAuthorsView.as_view()),
        path('feedback-top-filters-count/', FeedbackTopFiltersCountView.as_view(), name='feedback-top-filters-count'),

        # JWT
        path('auth/', include('userauth.urls')),

        # Swagger UI
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        re_path(r'^swagger.json$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger.yaml$', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),

        # path('ckeditor/', include('ckeditor_uploader.urls')),
    ])),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
