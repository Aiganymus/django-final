from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from core.models import Account
from users.models import MainUser, Profile
from utils.upload import delete_image


@receiver(post_save, sender=MainUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Account.objects.create(owner=instance)


@receiver(post_delete, sender=Profile)
def delete_avatar(sender, instance, **kwargs):
    if instance.avatar:
        delete_image(instance.avatar)
