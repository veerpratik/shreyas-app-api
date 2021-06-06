from django.db import models
from .vendor import Vendor


class Project(models.Model):
    vendorID = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    project_title = models.CharField(max_length=200,blank=True, null=True)
    project_budget = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
