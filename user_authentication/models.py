from django.db import models
from .utils import generate_id
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .utils import generate_id, generate_token
from .managers import CustomUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Permission, Group
import random




class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(primary_key=True, max_length=128, unique=True, default=generate_id)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(_("email address"), unique=True, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    username = models.CharField(max_length=255, unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=18, unique=True, blank=False, null=False)
    gender = models.CharField(max_length=6, null=False, blank=False)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=False, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, blank=False, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField('date_created', auto_now=True)
    user_permissions = models.ManyToManyField(Permission, related_name="user_auth_permission")
    groups = models.ManyToManyField(Group, related_name="user_auth_group")

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'User ID: {self.id} - Username: {self.username}'
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
    
    def save(self, *args, **kwargs):
        while not self.id:
            self.id = generate_id()
        return super().save(*args, **kwargs)
    

class UserProfile(models.Model):
    id = models.CharField(max_length=64, default=generate_id, primary_key=True)
    user = models.OneToOneField(User, related_name="user_rel", on_delete=models.CASCADE)
    #image = models.ImageField(upload_to="media/", blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    blood_group = models.CharField(max_length=5,  blank=True, null=True)
    height = models.DecimalField(max_digits=6, decimal_places=3,blank=True, null=True)
    weight = models.DecimalField(max_digits=6, decimal_places=3,blank=True, null=True)
    genotype = models.CharField(max_length=7,  blank=True, null=True)
    Medical_records = models.CharField(max_length=150, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField('date_created', auto_now=True)

    
    class Meta:
        ordering = ['-date_created']


class Token(models.Model):
    id = models.CharField(max_length=64, default=generate_id, primary_key=True)
    user = models.OneToOneField(User, related_name="user_token", on_delete=models.CASCADE)
    token = models.IntegerField(default=generate_token)
    date_created = models.DateTimeField(auto_now_add=True)
    expired = models.BooleanField(default=False)


    # def save(self, *args, **kwargs):
    #     if timezone.now() > self.date_created + timezone.timedelta(minutes=5):
    #         self.expired = True
    #         print(self.expired)
    #     super(Token, self).save(*args, **kwargs)




    class Meta:
        ordering = ['-date_created']
    

