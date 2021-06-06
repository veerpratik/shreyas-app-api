from django.contrib import admin
from common_account.models import Vendor, Project
from common_account.models.branch import Branch


class BranchAdmin(admin.ModelAdmin):
    list_display = ('id','branch_name', 'branch_city_name')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id','vendorID','project_title','project_budget',
                 'is_active','created_date','updated_date'
                   )


class VendorAdmin(admin.ModelAdmin):
    list_display = (
            'id', 'branchID','vendor_name','address','is_active',
            'created_date','updated_date'
        )                   


admin.site.register(Branch, BranchAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Vendor, VendorAdmin)
