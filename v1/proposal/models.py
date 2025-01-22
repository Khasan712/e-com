from django.db import models
from v1.user.models import Client
from v1.utilis.abstract_classes.abstract_classes import AbstractDefaultClass
from v1.utilis.enums import ObjectStatus, CompanyType


class Proposal(AbstractDefaultClass):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100)
    status = models.CharField(max_length=8, choices=ObjectStatus.choices(), default=ObjectStatus.choices()[0][0])
    inn = models.CharField(max_length=9, blank=True, null=True)
    pnfl = models.CharField(max_length=14, blank=True, null=True)
    user = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    json_data = models.JSONField(default=dict, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.phone_number
