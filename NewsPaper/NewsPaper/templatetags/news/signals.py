from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Post
from ...settings import DEFAULT_FROM_EMAIL


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        for category in instance.categories.all():
            for subscriber in category.subscribers.all():
                html_content = render_to_string('email/new_post.html', {
                    'post': instance,
                    'user': subscriber
                })
                send_mail(
                    subject=instance.title,
                    message='',
                    html_message=html_content,
                    from_email=DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email]
                )

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        html_content = render_to_string('email/welcome.html', {'user': instance})
        send_mail(
            subject='Добро пожаловать!',
            message='',
            html_message=html_content,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email]
        )