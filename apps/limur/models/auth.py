from django.contrib.auth.models import User
from django.db import models

from .organization import Organization


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='userprofile',
    )

    organization = models.ForeignKey(
        Organization, null=True, blank=True,
        help_text='Organization associated with user'
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='Phone number',
    )

    invalid_attemps_count = models.IntegerField(
        default=0,
        blank=True,
        help_text='Number of invalid login attempts',
    )

    lock_out_end = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Date time when account will be unlocked for logging in',
    )

    class Meta:
        db_table = 'userprofile'
