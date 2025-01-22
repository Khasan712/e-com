from django.urls import path
from v1.proposal.views.api_views import ProposalRegisterApi
app_name = 'v1_proposal_admin_urls'


urlpatterns = [
    path('', ProposalRegisterApi.as_view(),)
]
