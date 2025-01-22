from django.db import models
from django_relations.models import AbstractDefaultClass as AbsCLass


class AbstractDefaultClass(AbsCLass):
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

#    created_at = models.DateTimeField(auto_now_add=True)
#    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractBaseTitleClass(AbstractDefaultClass):
    title_ln = models.CharField(max_length=800, blank=True, null=True)
    title_kr = models.CharField(max_length=255, blank=True, null=True)
    title_ru = models.CharField(max_length=800, blank=True, null=True)
    title_en = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True


class AbstractBaseClass(AbstractBaseTitleClass):
    description_ln = models.CharField(max_length=300, blank=True, null=True)
    description_kr = models.CharField(max_length=300, blank=True, null=True)
    description_ru = models.CharField(max_length=300, blank=True, null=True)
    description_en = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        abstract = True
