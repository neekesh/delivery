
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from users.models import Order, UrgentDelivery, Notification
from .utils import change_fb_data


#checking if the status field is updated or not
@receiver(pre_save, sender=Order)
def track_order_updated(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Order.objects.get(pk=instance.pk)
        if instance.status != old_instance.status:
            notification = Notification.objects.get(order=old_instance)
            notification.order_status =   instance.status

            notification.save()

            change_fb_data(old_instance.user.email)

@receiver(post_save, sender=Order)
def track_order_created(sender, instance,created, **kwargs):
    if created:
            
        Notification.objects.create(
            order=instance,
            user = instance.user,
            order_status= instance.status,
        )
        change_fb_data(instance.user.email)
        
@receiver(post_save, sender=UrgentDelivery)
def track_delivery_crated(sender, instance,created, **kwargs):
    if created:
        Notification.objects.create(
            urgent_delivery=instance,
            user = instance.user,
            order_status= instance.status,
            )      
        change_fb_data(instance.user.email)

@receiver(pre_save, sender=UrgentDelivery)
def track_urgent_delivery_updated(sender, instance, **kwargs):
   if instance.pk:
        old_instance = UrgentDelivery.objects.get(pk=instance.pk)
        if instance.status != old_instance.status:
            notification = Notification.objects.get(urgent_delivery=old_instance)
            notification.order_status =   instance.status
            notification.save()
        change_fb_data(old_instance.user.email)
             