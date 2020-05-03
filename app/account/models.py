from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from trainer.models import Student, TakenQuiz

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.PositiveIntegerField(blank=True, default=0, verbose_name= 'Вопыт карыстальніка')
    image = models.ImageField(blank=True,
                              null = True,
                              width_field = "width_field",
                              height_field = "height_field",
                              default = "default.png",
                              upload_to = "profile_pics")

    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    birth_date = models.DateField(null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)

    #     img = Image.open(self.image.path)
    #     if img.height > 400 or img.width > 400:
    #         output_size = (400, 400)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_user_student(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
#Мы «зацепили» create_user_profile() и save_user_profile() к событию сохранения модели User.
#сигнала post_save.
@receiver(post_save, sender = TakenQuiz)
def add_score(instance, **kwargs):
    profile = instance.student.user.profile
    profile.experience += 10
    profile.save()