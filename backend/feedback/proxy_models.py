from django.utils.translation import gettext as _

from feedback.models import Feedback


class Comment(Feedback):
    class Meta:
        verbose_name = _('Комментарий')
        verbose_name_plural = _('Комментарии')
        proxy = True

    def __str__(self):
        if self.feedback_author and self.parent_feedback:
            return f'{self.feedback_author}::{self.parent_feedback.id}'
        else:
            return f'Comment({self.id})'
