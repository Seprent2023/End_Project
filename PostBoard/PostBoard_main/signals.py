from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives

from .models import Response
from django.contrib.auth.models import User


@receiver(post_init, sender=Response)
def pre(instance, **kwargs):
    instance.old_status = instance.status


@receiver(post_save, sender=Response)
def response_created(instance, created, raw, **kwargs):
    if created:
        user = User.objects.filter(email=instance.res_post.to_reg_user.reg_user.email)
        email = user[0].email

        subject = f'Новый отклик!'
        text_content = (
            f'К вашему посту {instance.res_post} был оставлен новый отклик! '
            f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.send()

    if instance.old_status != instance.status:
        user = User.objects.filter(email=instance.res_user.email)
        email = user[0].email
        subject = f'Отклик принят!'
        text_content = (
            f'Ваш отклик был принят автором поста! '
            f'Ссытка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.send()

