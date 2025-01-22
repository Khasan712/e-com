from django.contrib import admin
from .models import Proposal


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ("id", 'first_name', 'last_name', 'phone_number', 'created_at', 'status')
