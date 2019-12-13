from django.shortcuts import render
from rest_framework import viewsets
from firm.models import Firm, Worksite, Subcontractor, Contract
from .serializers import FirmSerializer, WorksiteSerializer, SubcontractorSerializer, ContractSerializer

class FirmView(viewsets.ModelViewSet):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer

class WorksiteView(viewsets.ModelViewSet):
    queryset = Worksite.objects.all()
    serializer_class = WorksiteSerializer

class SubcontractorView(viewsets.ModelViewSet):
    queryset = Subcontractor.objects.all()
    serializer_class = SubcontractorSerializer

class ContractView(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer