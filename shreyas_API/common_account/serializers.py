from rest_framework import serializers
from common_account.models.vendor import Vendor
from common_account.models.branch import Branch
from common_account.models.project import Project
from common_account.models.user import User


class BranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = ('id','branch_name', 'branch_city_name')
        read_only_fields = ('id',)


class VendorSerializer(serializers.ModelSerializer):
    branchID = serializers.PrimaryKeyRelatedField(
        # many=True,
        queryset=Branch.objects.all()
    )
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only = True)

    class Meta:
        model = Vendor
        fields = (
            'id', 'branchID','vendor_name','address','is_active',
            'created_date','updated_date', 'email', 'password'
        )

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        try:
             user = User.objects.create_vendor(email=email, password=password)
        except:
            raise serializers.ValidationError("this email is already exists")
        validated_data['user'] = user
    
        return Vendor.objects.create(**validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    vendorID = serializers.PrimaryKeyRelatedField(
        # many=True,
        queryset=Vendor.objects.all()
    )
    class Meta:
        model = Project
        fields = ('id','vendorID','project_title','project_budget',
                 'is_active','created_date','updated_date'
                 )
        read_only_fields = ('id',)  
