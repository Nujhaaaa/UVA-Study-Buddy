from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from allauth.account.signals import user_signed_up
from .models import user
import uuid


@receiver(user_signed_up)
def set_user_type(request, user, **kwargs):
    user_type = request.session.get('user_type', None)

    if user_type == 'student':
        user.user_type = 'student'
        user.is_tutor = False
    elif user_type == 'tutor':
        user.user_type = 'tutor'
        user.is_tutor = True

    # Preserve other arguments
    user.first_name = user.first_name
    user.last_name = user.last_name
    user.email = user.email
    user.password = uuid.uuid4().hex
    user.save()
