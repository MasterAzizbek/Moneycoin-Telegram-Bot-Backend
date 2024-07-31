from django.db import models
from django.contrib.auth.models import AbstractUser


class SocialMedia(models.Model):
    icon = models.CharField(max_length = 350)

    def __str__(self) -> str:
        return self.icon

class CustomUser(AbstractUser):
    username = models.CharField(max_length = 255, default="Player", unique=True)
    telegram_id = models.CharField(max_length = 100)
    first_name = models.CharField(max_length = 255)
    avatar = models.ImageField()
    is_admin = models.BooleanField(default = False)

    def __str__(self) -> str:
        return self.username
    
class Blum(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blum_amount = models.IntegerField(default=0)
    start_time = models.DateTimeField(blank=True, null=True)
    claim = models.BooleanField(default=False)
    daily_reward = models.BooleanField(default=False)
    date = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return self.user.username
    
class Tasks(models.Model):
    task_name = models.CharField(max_length = 255)
    task_prize_amount = models.IntegerField()
    task_url = models.URLField()
    task_icon = models.ForeignKey(SocialMedia, on_delete=models.CASCADE, blank=True, null=True)
    task_users = models.ManyToManyField(CustomUser, related_name="tasks_users", blank=True, null=True)
    task_status = models.BooleanField(default = True)

    def __str__(self) -> str:
        return f"{self.pk}. {self.task_name}"

class Invitation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    invite_link = models.CharField(max_length = 1000)
    invited_users = models.ManyToManyField(CustomUser, blank=True, related_name="invitation_users")

    def __str__(self) -> str:
        return self.user.username