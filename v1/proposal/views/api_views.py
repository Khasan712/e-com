from v1.proposal.serializers.api_serializers import ProposalSerializer
from v1.utilis.mixins.generic_mixins import CustomCreateAPIView


class ProposalRegisterApi(CustomCreateAPIView,):
    serializer_class = ProposalSerializer

