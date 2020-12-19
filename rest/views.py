from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from firm.models import Firm, Worksite, Subcontractor, Contract, Specification, Project
from progress.models import Discovery, Analysis, AnalysisDetail, Progress, Synopsis
from .serializers import FirmSerializer, WorksiteSerializer, SubcontractorSerializer, ContractSerializer, SpecificationSerializer, ProjectSerializer, DiscoverySerializer, AnalysisSerializer, AnalysisDetailSerializer, ProgressSerializer, SynopsisSerializer

class FirmViewSet(viewsets.ModelViewSet):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer
    permission_classes = [DjangoModelPermissions]
    throttle_scope = 'toManyPost'

    def get_queryset(self):
        queryset = Firm.objects.filter(pk=self.request.user.firm.pk)
        return queryset


class WorksiteViewSet(viewsets.ModelViewSet):
    queryset = Worksite.objects.all()
    serializer_class = WorksiteSerializer
    permission_classes = [DjangoModelPermissions]
    throttle_scope = 'toManyPost'

    def get_queryset(self):
        queryset = Worksite.objects.filter(firm_id=self.request.user.firm.pk)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(firm=Firm.objects.get(pk=self.request.user.firm.pk))


class SubcontractorViewSet(viewsets.ModelViewSet):
    queryset = Subcontractor.objects.all()
    serializer_class = SubcontractorSerializer
    permission_classes = [DjangoModelPermissions]
    throttle_scope = 'toManyPost'


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [DjangoModelPermissions]
    throttle_scope = 'toManyPost'


class SpecificationViewSet(viewsets.ModelViewSet):
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer
    permission_classes = [DjangoModelPermissions]
    throttle_scope = 'toManyPost'


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [DjangoModelPermissions]
    throttle_scope = 'toManyPost'


class DiscoveryViewSet(viewsets.ModelViewSet):
    queryset = Discovery.objects.all()
    serializer_class = DiscoverySerializer
    permission_classes = [DjangoModelPermissions]
    throttle_scope = 'toManyPost'

class AnalysisViewSet(viewsets.ModelViewSet):
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer
    permission_classes = [DjangoModelPermissions]
    throttle_scope = 'toManyPost'


class AnalysisDetailViewSet(viewsets.ModelViewSet):
    queryset = AnalysisDetail.objects.all()
    serializer_class = AnalysisDetailSerializer
    permission_classes = [DjangoModelPermissions]
    throttle_scope = 'toManyPost'


class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    permission_classes = [DjangoModelPermissions]
    throttle_scope = 'toManyPost'


class SynopsisViewSet(viewsets.ModelViewSet):
    queryset = Synopsis.objects.all()
    serializer_class = SynopsisSerializer
    permission_classes = [DjangoModelPermissions]
    throttle_scope = 'toManyPost'