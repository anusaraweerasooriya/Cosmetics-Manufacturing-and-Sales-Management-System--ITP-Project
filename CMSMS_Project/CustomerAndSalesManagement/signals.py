from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from DeliveryManagement.models import *
from .models import *


# @receiver(post_save, sender=Customer)
def create_customer(sender, instance, created, **kwargs):
    print('Profile signal triggered')
    if created:
        user = instance
        customer = Customer.objects.create(
            user=user,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            email=user.email,

        )


def update_customer(sender, instance, created, **kwargs):
    customer = instance
    user = customer.user

    if not created:
        user.first_name = customer.first_name
        user.last_name = customer.last_name
        user.username = customer.username
        user.email = customer.email
        user.save()


def delete_customer(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    print('Deleting a customer')


post_save.connect(create_customer, sender=User)
post_save.connect(update_customer, sender=Customer)
post_delete.connect(delete_customer, sender=Customer)
