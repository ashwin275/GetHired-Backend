from django.contrib import admin
from .models import Account , UserProfile
from django.contrib.auth import get_user_model

# User = get_user_model()

# admin.site.unregister(User)


admin.site.register(Account)
admin.site.register(UserProfile)