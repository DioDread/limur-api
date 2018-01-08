from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from limur.models.organization import Organization


class UserProfile(models.Model):
    ORG_ACCESS_OWNER = 'owner'
    ORG_ACCESS_ADMIN = 'admin'
    ORG_ACCESS_NONE = None

    ORG_ACCESS_CHOICES = (
        (ORG_ACCESS_OWNER, 'Owner',),
        (ORG_ACCESS_ADMIN, 'Administrator',),
        (ORG_ACCESS_NONE, 'None'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='userprofile',
    )

    # TODO Probably should be a M2M relation through org access table
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

    is_moderator = models.BooleanField(
        default=False,
        help_text='Moderator role enabled',
    )

    # TODO Probably should be moved to M2M link table
    org_access_level = models.CharField(
        max_length=8,
        null=True,
        blank=True,
        default=None,
        choices=ORG_ACCESS_CHOICES
    )

    class Meta:
        db_table = 'userprofile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
