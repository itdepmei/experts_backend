from django.urls import path
from .views import *

urlpatterns = [
    path('reports/', ReportAPIView.as_view(), name='report-list'),  # For listing reports
    path('reports/<str:uuid>/', ReportAPIView.as_view(), name='report-detail'),  # For fetching a report by UUID
    path('committee-members/', CommitteeMemberView.as_view(), name='committee-members'),
    path('committee-members/<str:uuid>/', CommitteeMemberView.as_view(), name='committee-member-detail'),
    path('committee-members/section/<str:uuid>/', CommitteeMemberBySection.as_view(), name='committee-member-by-section'),
]
