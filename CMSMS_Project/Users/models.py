from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bio = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    image = models.ImageField(default='avatar.png', upload_to='Profile_images', null=True, blank=True)

    def __str__(self):
        return f'{self.staff.username} - Profile'
