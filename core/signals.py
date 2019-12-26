# from django.db.models.signals import pre_save
# from django.dispatch import receiver
#
# from core.models import Account
#
#
# @receiver(pre_save, sender=Account)
# def do_something_if_changed(sender, instance, **kwargs):
#     try:
#         obj = sender.objects.get(number=instance.number)
#     except sender.DoesNotExist:
#         return
#     if obj.account_type != instance.account_type:
#         if instance.account_type == 0:
#             instance.monthly_fee = 100
#             instance.save()
