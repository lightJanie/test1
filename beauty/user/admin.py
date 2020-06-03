from django.contrib import admin

# Register your models here.
from .models import UserProfile,Address
admin.site.register(UserProfile)
admin.site.register(Address)

# admin superuser
#账户名：admin
#密码：1024asdf