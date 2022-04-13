from django.core.validators import RegexValidator
from django.db import models
from projects.models import *
from django.contrib.auth import authenticate,get_user_model
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12,validators=[RegexValidator(regex='^01[0|1|2|5][0-9]{8}$',message='Phone must be start 010, 011, 012, 015 and all number contains 11 digits',code='invalid number') ])
    birth = models.DateField(null=True)
    social_media = models.URLField()
    country = models.CharField(max_length=40)
    is_active=models.IntegerField()
    image = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return f'{self.user.username} '

class Donation (models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    project_id=models.ForeignKey('projects.Projects',on_delete=models.CASCADE)
    amount_of_money = models.FloatField()
    def __str__(self):
        return "User Id"+str(self.user_id)

class Comment (models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    project_id = models.ForeignKey('projects.Projects', on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return "Comment Id"+str(self.user_id)

class Replay (models.Model):
    comment_id = models.ForeignKey('Comment', on_delete=models.CASCADE)
    replay = models.TextField()
    def __str__(self):
        return "Comment Id"+str(self.user_id)

class Reportno (models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_id = models.ForeignKey('Comment', on_delete=models.CASCADE)
    def __str__(self):
        return "User Id"+str(self.user_id)