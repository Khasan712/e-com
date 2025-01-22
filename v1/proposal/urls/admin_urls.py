from django.urls import path
from v1.proposal.views.admin_views import ProposalApi, ProposalDetailApi

app_name = 'v1_proposal_admin_urls'


urlpatterns = [
    path('', ProposalApi.as_view()),
    path('<int:pk>/', ProposalDetailApi.as_view()),
]
