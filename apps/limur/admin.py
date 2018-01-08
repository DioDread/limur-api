from django.contrib import admin
from limur.models import UserProfile, Organization

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization']

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Organization, OrganizationAdmin)
