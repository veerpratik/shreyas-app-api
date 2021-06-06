from django.urls import path
from common_account.views import common_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path('login/',common_views.CustomTokenObtainPairView.as_view(), name = 'login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('vendor_list/', common_views.VendorList.as_view(), name = 'vendor_list'),
    path('vendor_details/<int:pk>/', common_views.VendorDetail.as_view(), name="vendor_details"),
    path('vendor_summary/', common_views.VendorSummary.as_view(), name='vendor_summary'),
    path('branch_list/', common_views.BranchList.as_view(), name='branch_list'),
    path('branch_details/<int:pk>/', common_views.BranchDetailView.as_view(), name="branch_details"),
    path('project_list/', common_views.ProjectList.as_view(), name='project_list')
  
]
