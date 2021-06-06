from django.db import models


class Branch(models.Model):
    branch_name = models.CharField(max_length=200,blank=True, null=True)
    branch_city_name = models.CharField(max_length=200,blank=True, null=True)
