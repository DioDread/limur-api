from django.db import models


class Organization(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )

    is_demo = models.BooleanField(default=False)
    is_validated = models.BooleanField(default=False)

    class Meta:
        db_table = 'organization'


class PerOrganizationMixin(models.Model):
    organization = models.ForeignKey(
        Organization,
    )

    class Meta:
        abstract = True
