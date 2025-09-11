from djoser import utils
from djoser.conf import settings as djoser_settings
from django.contrib.auth.tokens import default_token_generator
from djoser.email import BaseDjoserEmail


class UserChangePasswordNotificationMail(BaseDjoserEmail):
    """Send a confirmation email to user about change his password to new."""
    template_name = "email/password_set_confirmation.html"

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")

        context.update({
            "uid": utils.encode_uid(user.pk),
            "token": default_token_generator.make_token(user),
            "url": djoser_settings.PASSWORD_SET_CONFIRM_URL.format(**context)
        })
        return context


class UserSuccessChangePasswordNotificationMail(BaseDjoserEmail):
    """Send a confirmation email to user about change his password to new."""
    template_name = "email/password_change_success.html"

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")

        context.update({
            "uid": utils.encode_uid(user.pk),
            "token": default_token_generator.make_token(user),
            "url": djoser_settings.PASSWORD_SET_CONFIRM_URL.format(**context)
        })
        return context


class UserChangeEmailNotificationMail(BaseDjoserEmail):
    """Send a confirmation email to user about change his current email address."""
    template_name = "email/email_set_confirmation.html"

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")

        context.update({
            "uid": utils.encode_uid(user.pk),
            "token": default_token_generator.make_token(user),
            "url": djoser_settings.EMAIL_SET_CONFIRM_URL.format(**context)
        })
        return context


class UserChangeEmailOldNotification(BaseDjoserEmail):
    """Send a user confirmation to old email to user about change his current email address."""
    template_name = "email/email_set_old_email_notification.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["new_email"] = self.context.get("new_email")
        return context


class UserSuccessEmailChangeNotificationMail(BaseDjoserEmail):
    """Notify about successful email change"""
    template_name = "email/email_change_success.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["new_email"] = self.context.get("new_email")
        return context
