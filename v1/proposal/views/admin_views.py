from rest_framework.exceptions import NotFound

from v1.utilis.custom_responses import params_error_repsonse, success_response
from v1.utilis.enums import ObjectStatus
from v1.utilis.querysets.get_active_querysets import get_active_proposals
from rest_framework.pagination import PageNumberPagination
from v1.proposal.serializers.admin_serializers import ProposalSerializer
from v1.utilis.mixins.generic_mixins import CustomDeleteAPIView, CustomListAPIView, CustomRetrieveAPIView, CustomUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q


class ProposalApi(CustomListAPIView, APIView):
    serializer_class = ProposalSerializer
    queryset = get_active_proposals()
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        q = self.request.query_params.get('q')
        if status:
            if not status in list(ObjectStatus.choices()):
                return Response(params_error_repsonse())
            queryset = queryset.filter(status=status)
        if q:
            queryset = queryset.filter(
                Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(phone_number__icontains=q) |
                Q(inn__icontains=q) | Q(status__icontains=q)
            )
        return queryset

    def patch(self, request, *args, **kwargs):
        status = self.request.query_params.get("status")
        proposal_id = request.query_params.get("proposal_id")
        if not proposal_id or not status:
            return Response(params_error_repsonse('status', 'proposal_id'))
        proposal = get_active_proposals().filter(id=proposal_id).first()
        serializer = self.serializer_class(data=request.data, instance=proposal, partial=True, context={'status': status})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(success_response())


class ProposalDetailApi(CustomRetrieveAPIView, CustomUpdateAPIView, CustomDeleteAPIView):
    serializer_class = ProposalSerializer
    queryset = get_active_proposals()
    pagination_class = PageNumberPagination
