import base64
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import Consumer

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=Consumer)
def generate_hash(sender, instance=None, created=False, **kwargs):
    if created:
        encodedBytes = base64.urlsafe_b64encode(instance.user.username.encode("utf-8"))
        instance.user_hash = str(encodedBytes, "utf-8")
        instance.save(update_fields=['user_hash'])
