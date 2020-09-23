from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    objects = UserManager()


class ratings(models.Model):
  """docstring for ratings"""
  review = models.CharField(max_length=200)
  rating = models.IntegerField(default=0)
  reviewedby = models.CharField(max_length=200)
  courseid = models.CharField(max_length=200)
    