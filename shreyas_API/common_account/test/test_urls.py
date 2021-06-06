from django.test import SimpleTestCase
from django.urls import reverse, resolve
from common_account.views.common_views import *


class TestUrls(SimpleTestCase):

    def test_login_url_resolve(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, CustomTokenObtainPairView)

    def test_vendor_list_url_resolve(self):
        url = reverse('vendor_list')
        self.assertEquals(resolve(url).func.view_class, VendorList)

    def test_vendor_detail_url_resolve(self):
        url = reverse('vendor_details', args=[1])
        self.assertEquals(resolve(url).func.view_class, VendorDetail)

    def test_vendor_summary_url_resolve(self):
        url = reverse('vendor_summary')
        self.assertEquals(resolve(url).func.view_class, VendorSummary)    

    def test_branch_list_url_resolve(self):
        url = reverse('branch_list')
        self.assertEquals(resolve(url).func.view_class, BranchList)

    def test_branch_detail_url_resolve(self):
        url = reverse('branch_details', args=[1])
        self.assertEquals(resolve(url).func.view_class, BranchDetailView)
       
    def test_project_list_url_resolve(self):
        url = reverse('project_list')
        self.assertEquals(resolve(url).func.view_class, ProjectList)    