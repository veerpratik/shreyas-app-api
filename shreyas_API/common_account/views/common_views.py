from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import generics

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['name'] = user.email
        return token
   

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common_account.models import Vendor, Project
from common_account.models.branch import Branch
from common_account.serializers import VendorSerializer, BranchSerializer, ProjectSerializer
from common_account import constants
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from common_account.helper import paginate
from django.db.models import Q, F
from django.db.models import Avg, Sum


class VendorList(APIView):
    """
    List all vendorss, or create a new vendor.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = VendorSerializer
    
    def get(self,request,format = None):
        context_data = dict()
        page_no = request.GET.get('page', 1)
        page_offset = request.GET.get('offset', 20)
        queryset = Vendor.objects.select_related('branchID').filter().order_by('-id')
        search = request.GET.get('q', '')
        if search:
            queryset = queryset.filter(Q(branchID=search) | Q(
                vendor_name__icontains=search))
                

        serializer = VendorSerializer(queryset, many=True)
        data, context_data = paginate(
            serializer.data, page_no, page_offset=page_offset)

        context_data[constants.RESPONSE_RESULT] = data.object_list
        context_data[constants.RESPONSE_ERROR] = False
        context_data[constants.RESPONSE_MESSAGE] = 'Register list retrieved successfully.'
        return Response(context_data)

    def post(self, request, format=None):
        context_data = dict()
        data = JSONParser().parse(request)
        error = False
        msg = ''
        email = data.get('email', None)
        branchID = data.get('branchID', None)
        vendor_name = data.get('vendor_name', None)
        address = data.get('address')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if not email:
            error = True
            msg = 'email is required'
        if not error and not  branchID:
            error = True
            msg = ' Branch name is required'
        if not error and not vendor_name:
            error = True
            msg = 'Vendor name is required'
        if not error and not address:
            error = True
            msg = 'Vendor address is required'    
        if not error and not password:
            error = True
            msg = "Password is required."     
        if not error and not confirm_password:
            error = True
            msg = "confirm_password is required."
        if not error and password != confirm_password:
            error = True
            msg = 'Password mismatch'    

        if not error:
            obj  = Vendor.objects.filter(user__email = email).first()
            if obj:
                context_data[constants.RESPONSE_ERROR] = True
                context_data[constants.RESPONSE_MESSAGE] = 'This email has already registered'
                return Response(context_data)
  
            serializer = VendorSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                context_data[constants.RESPONSE_RESULT] = serializer.data
                context_data[constants.RESPONSE_ERROR] = False
                context_data[constants.RESPONSE_MESSAGE] = 'New Vendor added successfully.'
                return Response(context_data)
               
            else:
                context_data[constants.RESPONSE_ERROR] = True
                context_data[constants.RESPONSE_MESSAGE] = serializer.errors
                
        else:
            context_data[constants.RESPONSE_ERROR] = True
            context_data[constants.RESPONSE_MESSAGE] = msg
        return Response(context_data, status=status.HTTP_400_BAD_REQUEST)


class VendorDetail(APIView):
    """
    Retrieve, update or delete a vendor instance.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = VendorSerializer

    def get_object(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        context_data = dict()
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor)
        context_data[constants.RESPONSE_RESULT] = serializer.data
        context_data[constants.RESPONSE_MESSAGE] = 'Vendorretrived succesfully.'
        return Response(context_data)

    def put(self, request, pk, format=None):
        vendor = self.get_object(pk)
        context_data = dict()
        serializer = VendorSerializer(vendor, data=JSONParser().parse(request))
        if serializer.is_valid():
            serializer.save()
            context_data[constants.RESPONSE_RESULT] = serializer.data
            context_data[constants.RESPONSE_ERROR] = False
            context_data[constants.RESPONSE_MESSAGE] = 'Vendor updated succesfully.'
            return Response(context_data)
        context_data[constants.RESPONSE_ERROR] = True
        context_data[constants.RESPONSE_MESSAGE] = serializer.errors    
        return Response(context_data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        vendor = self.get_object(pk)
        context_data = dict()
        vendor.delete()
        context_data[constants.RESPONSE_ERROR] = False
        context_data[constants.RESPONSE_MESSAGE] = 'Vendor deleted succesfully.'
        return Response(context_data, status=status.HTTP_204_NO_CONTENT)


class VendorSummary(APIView):
    """
    Get summary of vendor.
    """
    permission_classes = [IsAuthenticated]
   
    def get(self, request, format=None):
        context_data = dict()
        vendor_name = request.GET.get('vendor_name',None)
        branch_name = request.GET.get('branch_name',None)

        try:
            if vendor_name and branch_name is None:
                queryset = Project.objects.filter(vendorID__vendor_name__icontains = vendor_name).aggregate(avg_budget = Avg('project_budget'),
                total_budget = Sum('project_budget'))

            if vendor_name and branch_name:
                queryset = Project.objects.filter(Q(vendorID__vendor_name__icontains = vendor_name) &
                Q(vendorID__branchID__branch_name__icontains =  branch_name)).aggregate(avg_budget = Avg('project_budget'),
                total_budget = Sum('project_budget'))    

            context_data[constants.RESPONSE_RESULT] = queryset
            context_data[constants.RESPONSE_MESSAGE] = 'Vendor Summary retrived.'

        except Vendor.DoesNotExist:
            raise Http404    
             
        return Response(context_data)


class BranchList(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]


class BranchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]


class ProjectList(APIView):
    """
    List all projects, or create a new project.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer
    
    def get(self,request,format = None):
        context_data = dict()
        page_no = request.GET.get('page', 1)
        page_offset = request.GET.get('offset', 20)
        queryset = Project.objects.select_related('vendorID',).filter().order_by('-id')
        search = request.GET.get('q', '')
        if search:
            queryset = queryset.filter(Q(vendorID__vendor_name__icontains=search) | Q(
                project_title__icontains=search))

        serializer = ProjectSerializer(queryset, many=True)
        data, context_data = paginate(
            serializer.data, page_no, page_offset=page_offset)

        context_data[constants.RESPONSE_RESULT] = data.object_list
        context_data[constants.RESPONSE_ERROR] = False
        context_data[constants.RESPONSE_MESSAGE] = 'Project list retrieved successfully.'
        return Response(context_data)

    def post(self, request, format=None):
        context_data = dict()
        data = JSONParser().parse(request)
        error = False
        msg = ''

        vendorID = data.get('vendorID', None)
        project_title = data.get('project_title', None)
        project_budget = data.get('project_budget')
        
        if not vendorID:
            error = True
            msg = 'Vendor is required'
        if not error and not project_title:
            error = True
            msg = 'Project title is required'
        if not error and not project_budget:
            error = True
            msg = 'Project budget is required'    
        if not error:
            obj  = Project.objects.filter(project_title__icontains = project_title).first()
            if obj:
                context_data[constants.RESPONSE_ERROR] = True
                context_data[constants.RESPONSE_MESSAGE] = 'This Project title has already registered'
                return Response(context_data)
  
            serializer = ProjectSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                context_data[constants.RESPONSE_RESULT] = serializer.data
                context_data[constants.RESPONSE_ERROR] = False
                context_data[constants.RESPONSE_MESSAGE] = 'New Project added successfully.'
                return Response(context_data)
               
            else:
                context_data[constants.RESPONSE_ERROR] = True
                context_data[constants.RESPONSE_MESSAGE] = serializer.errors
                
        else:
            context_data[constants.RESPONSE_ERROR] = True
            context_data[constants.RESPONSE_MESSAGE] = msg
        return Response(context_data, status=status.HTTP_400_BAD_REQUEST)        
