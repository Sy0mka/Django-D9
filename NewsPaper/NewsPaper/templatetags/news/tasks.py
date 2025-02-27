from celery import shared_task
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from .models import Category

@shared_task
def weekly_digest():
    for category in Category.objects.all():
        subscribers = category.subscribers.all()
        if subscribers.exists():
            posts = category.post_set.filter(created_at__gte=timezone.now()-timedelta(days=7))
            html_content = render_to_string('email/weekly_digest.html', {
                'category': category,
                'posts': posts
            })
            send_mail(
                subject=f'Новые статьи в категории {category.name}',
                message='',
                html_message=html_content,
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber.email for subscriber in subscribers]
            )