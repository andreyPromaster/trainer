from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.PositiveIntegerField(blank=True, default=0, verbose_name= 'Вопыт карыстальніка')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
#Мы «зацепили» create_user_profile() и save_user_profile() к событию сохранения модели User. сигнала post_save.
#код из доков