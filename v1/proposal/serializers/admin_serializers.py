from rest_framework import serializers
from v1.proposal.models import Proposal
from v1.user.serializers.admin_serializers import ClientSerializer
from django.db import transaction
from v1.user.models import Client


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = (
            'id', 'first_name', 'last_name', 'phone_number', 'json_data', 'comment',
            'status', 'inn', 'pnfl', 'created_at', "update_at"
        )
    
    def update(self, instance, validated_data):
        status = self.context.get('status')
        if status == 'accepted':
            with transaction.atomic():
                data = {
                    "first_name": instance.first_name,
                    "last_name": instance.last_name,
                    "phone_number": instance.phone_number,
                    "password1": instance.phone_number,
                    "password2": instance.phone_number
                }
                client_serialzier = ClientSerializer(data=data)
                client_serialzier.is_valid(raise_exception=True)
                client_serialzier.save()
                instance.user = Client.objects.get(id=client_serialzier.data.get("id"))
        instance.status=status
        instance.save()
        return validated_data


class ProposalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = (
            'id', 'first_name', 'last_name', 'phone_number', 'json_data',
            'status', 'inn', 'pnfl', 'created_at', "update_at"
        )

