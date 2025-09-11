# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.conf import settings
#
# from author.models import Author
# from student.models import Student
#
#
#
#
# def send_notification_email(user):
#     """function for sending email to user"""
#     subject = f"Зарегистрирован новый {'Автор' if isinstance(user, Author) else 'Студент'}"
#     message = f"Зарегистрирован новый {'Автор' if isinstance(user, Author) else 'Студент'}: {user.email}"
#     print(message)
#     recipient_list = settings.ADMINS.split(",")
#     if recipient_list:
#         send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
#
# @receiver(post_save, sender=Author)
# @receiver(post_save, sender=Student)
# def user_registered_handler(sender, instance, created, **kwargs):
#     """Signal handler for user registration"""
#     if created:
#         send_notification_email(instance)
