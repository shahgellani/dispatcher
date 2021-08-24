from django.contrib.auth.models import PermissionsMixin

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


# Create your models here.


class UserManager():

    def males(self):
        return self.all().filter(gender=self.GENDER_MALE)

    def females(self):
        return self.all().filter(gender=self.GENDER_FEMALE)


class Employee(models.Model):
    """
    Employee/User table
    """
    email = models.EmailField(max_length=32)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    password = models.CharField(max_length=32, default=None)
    age = models.IntegerField(default=0)
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1)


class Dispatches(models.Model):
    """
    Dispatches Table
    """
    driver = models.ForeignKey(Employee, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    pickup_location = models.CharField(max_length=32, default=None)
    delivery_location = models.CharField(max_length=32, default=None)
    status = models.CharField(max_length=32, choices=[('In Transit', 'In-Transit'), ('Delivered', 'Delivered')])
    arrival_date = models.DateTimeField(blank=True, null=True)
    departure_date = models.DateTimeField(blank=True, null=True)


class POD(models.Model):
    dispatch = models.ForeignKey(Dispatches, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/', null=True)
