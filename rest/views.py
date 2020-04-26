from rest_framework import viewsets
from firm.models import Firm, Worksite, Subcontractor, Contract, Specification, Project
from progress.models import Discovery, Analysis, AnalysisDetail, Progress, Synopsis
from .serializers import FirmSerializer, WorksiteSerializer, SubcontractorSerializer, ContractSerializer, SpecificationSerializer, ProjectSerializer, DiscoverySerializer, AnalysisSerializer, AnalysisDetailSerializer, ProgressSerializer, SynopsisSerializer


class FirmViewSet(viewsets.ModelViewSet):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer

class WorksiteViewSet(viewsets.ModelViewSet):
    queryset = Worksite.objects.all()
    serializer_class = WorksiteSerializer

class SubcontractorViewSet(viewsets.ModelViewSet):
    queryset = Subcontractor.objects.all()
    serializer_class = SubcontractorSerializer

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

class SpecificationViewSet(viewsets.ModelViewSet):
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class DiscoveryViewSet(viewsets.ModelViewSet):
    queryset = Discovery.objects.all()
    serializer_class = DiscoverySerializer

class AnalysisViewSet(viewsets.ModelViewSet):
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer

class AnalysisDetailViewSet(viewsets.ModelViewSet):
    queryset = AnalysisDetail.objects.all()
    serializer_class = AnalysisDetailSerializer

class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer

class SynopsisViewSet(viewsets.ModelViewSet):
    queryset = Synopsis.objects.all()
    serializer_class = SynopsisSerializer