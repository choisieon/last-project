from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.
# user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='accounts_profile')


class User(AbstractUser):
    pass

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     nickname = models.CharField(max_length=20)
#     age_range = models.CharField(max_length=20, choices=[
#         ('10s', '10대'), ('20s', '20대'), ('30s', '30대 이상')
#     ])
#     bio = models.TextField(blank=True)

#     def __str__(self):
#         return self.nickname
    

