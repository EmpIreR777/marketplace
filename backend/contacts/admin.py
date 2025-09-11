from django.contrib.admin import register
from django.db import models
from unfold import admin
from unfold.contrib.filters.admin import RangeDateTimeFilter
from unfold.contrib.forms.widgets import WysiwygWidget

from contacts.models import Contact


@register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_read', 'created_at')
    list_editable = ('is_read',)
    ordering = ('-created_at',)

    search_fields = ('email', 'name')
    list_filter_submit = True
    list_filter = ('is_read', ('created_at', RangeDateTimeFilter))

    readonly_fields = ('created_at',)
    fields = ('email', 'is_read', 'name', 'message', 'created_at')
    formfield_overrides = {
        models.TextField: {'widget': WysiwygWidget},
    }
