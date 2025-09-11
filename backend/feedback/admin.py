from django.contrib.admin import register
from unfold import admin
from unfold.contrib.filters.admin import RangeDateTimeFilter
from unfold.decorators import display

from feedback.models import Feedback
from feedback.proxy_models import Comment


##############################################################################################################
# Inlines
##############################################################################################################
class CommentInline(admin.TabularInline):
    model = Comment
    fields = ('id', 'feedback_author', 'short_text')
    readonly_fields = ('short_text',)
    extra = 1
    show_change_link = True
    tab = True

    @display(description='Текст')
    def short_text(self, obj):
        return obj.feedback_text[:20]


##############################################################################################################
# Admin Models
##############################################################################################################
@register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_author', 'feedback_to_course', 'feedback_rating', 'is_approved',
                    'feedback_date')
    list_editable = ('is_approved',)
    ordering = ('-feedback_date',)

    search_fields = ('feedback_author__email',)
    list_filter_submit = True
    list_filter = ('is_approved', 'feedback_rating', ('feedback_date', RangeDateTimeFilter))

    readonly_fields = ('feedback_date',)
    fields = ('feedback_author', 'feedback_to_course', 'feedback_rating', 'feedback_text', 'is_approved',
              'feedback_date')

    autocomplete_fields = ('feedback_author', 'feedback_to_course')
    inlines = (CommentInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent_feedback__isnull=True)


@register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('feedback_author', 'parent_feedback', 'is_approved', 'feedback_date')
    list_editable = ('is_approved',)
    ordering = ('parent_feedback', '-feedback_date',)

    search_fields = ('feedback_author__email',)
    list_filter_submit = True
    list_filter = ('is_approved', ('feedback_date', RangeDateTimeFilter))

    readonly_fields = ('feedback_date',)
    fields = ('feedback_author', 'parent_feedback', 'feedback_text', 'is_approved', 'feedback_date')

    autocomplete_fields = ('feedback_author', 'parent_feedback')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent_feedback__isnull=False)
