from django.contrib import admin
from .models import User, UserProfile, Token

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Token)
# Register your models here.
