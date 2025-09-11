from django.contrib.admin import register
from django.db import models
from unfold import admin
from unfold.contrib.filters.admin import RangeDateTimeFilter
from unfold.contrib.forms.widgets import WysiwygWidget

from notification.models import Notification


##############################################################################################################
# Admin Models
##############################################################################################################
@register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_read', 'notification_type', 'created_at')
    list_editable = ('is_read',)
    ordering = ('-created_at',)

    search_fields = ('title', 'user__email')
    list_filter_submit = True
    list_filter = ('is_read', 'notification_type', ('created_at', RangeDateTimeFilter))

    autocomplete_fields = ('user',)

    readonly_fields = ('created_at',)
    fields = ('title', 'user', 'body', 'html', 'is_read', 'notification_type', 'created_at')
    formfield_overrides = {
        models.TextField: {'widget': WysiwygWidget},
    }
    
