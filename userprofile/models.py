from django.db import models
from django.db.models.signals import post_save

from authentication.models import Account


def get_profile_image_filepath(self, filename):
    return f'profile_images/{str(self.pk)}/{"profile_image.png"}'

def get_default_profile_image():
    return 'img/avatar.jpg'


class Profile(models.Model):
    staff = models.OneToOneField(Account, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)
    # image = models.ImageField(default='avatar.jpg', upload_to='Profile_Images', null=True)
    job_function = models.CharField(max_length=200, null=True)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True,
                                      default=get_default_profile_image)

    def __str__(self):
        return f'{self.staff.username}-Profile'

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(staff=instance)


post_save.connect(post_user_created_signal, sender=Account)
