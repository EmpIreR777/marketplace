from django.contrib.admin import register
from unfold import admin

from questions.models import Answer, Question


##############################################################################################################
# Inlines
##############################################################################################################
class AnswerInline(admin.StackedInline):
    model = Answer
    fields = ('id', 'text', 'answer_category', 'openness_priority')
    readonly_fields = ('id',)
    extra = 1
    tab = True
    can_delete = True


##############################################################################################################
# Admin Models
##############################################################################################################
@register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'has_multiple_answers')
    list_editable = ('has_multiple_answers',)
    ordering = ('title',)

    search_fields = ('title', 'text')
    list_filter_submit = True
    list_filter = ('has_multiple_answers',)

    fields = ('title', 'text', 'has_multiple_answers')

    inlines = (AnswerInline,)
