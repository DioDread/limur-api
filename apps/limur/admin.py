from django.contrib import admin
from limur.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization']

admin.site.register(UserProfile, UserProfileAdmin)
