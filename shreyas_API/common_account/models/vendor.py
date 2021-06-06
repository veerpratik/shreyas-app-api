from django.db import models
from .branch import Branch


class Vendor(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    branchID = models.ForeignKey('Branch', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=200,blank=True, null=True)
    address = models.CharField(max_length = 200,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)