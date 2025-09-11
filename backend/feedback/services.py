from django.utils.timezone import now
from datetime import timedelta, datetime


class FeedbackService:
    @staticmethod
    def time_since_review(created_at: datetime) -> str:
        """Return how much time ago created_at was"""

        delta = now() - created_at

        if delta < timedelta(minutes=1):
            return "меньше минуты назад"
        elif delta < timedelta(hours=1):
            minutes = delta.seconds // 60
            return f"{minutes} {'минуту' if minutes == 1 else 'минуты' if 2 <= minutes <= 4 else 'минут'} назад"
        elif delta < timedelta(days=1):
            hours = delta.seconds // 3600
            return f"{hours} {'час' if hours == 1 else 'часа' if 2 <= hours <= 4 else 'часов'} назад"
        elif delta < timedelta(days=7):
            days = delta.days
            return f"{days} {'день' if days == 1 else 'дня' if 2 <= days <= 4 else 'дней'} назад"
        elif delta < timedelta(days=30):
            weeks = delta.days // 7
            return f"{weeks} {'неделю' if weeks == 1 else 'недели' if 2 <= weeks <= 4 else 'недель'} назад"
        elif delta < timedelta(days=365):
            months = delta.days // 30
            return f"{months} {'месяц' if months == 1 else 'месяца' if 2 <= months <= 4 else 'месяцев'} назад"
        else:
            years = delta.days // 365
            return f"{years} {'год' if years == 1 else 'года' if 2 <= years <= 4 else 'лет'} назад"
