from rest_framework import serializers
from firm.models import Firm, Worksite, Subcontractor, Contract, Specification, Project
from progress.models import Discovery, Analysis, AnalysisDetail, Progress, Synopsis

class FirmSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Firm
        fields = ['url','tax','name','full_name','phone','fax','web','email','address','image']

class WorksiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Worksite
        fields = ['url','name','employer','name_of_job','control','construction_area','threader_no','island_no','parcel_no','phone','fax','address','image','start_date','end_date','active']

class SubcontractorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subcontractor
        fields = ['url','worksite','name','email','phone','subject','address']

class ContractSerializer(serializers.HyperlinkedModelSerializer):
    #subcontractor = serializers.HyperlinkedRelatedField(many=True, view_name='subcontractor', read_only=True)

    class Meta:
        model = Contract
        fields = ['url','worksite','subcontractor','no','date','name','price','guarantee','advance','progress','note','file']

class SpecificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Specification
        fields = ['url','contract','name','file']

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ['url','worksite','no','date','name','category','file']

class DiscoverySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Discovery
        fields = ['url','worksite','no','name','unit','amount','price','total']

class AnalysisSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Analysis
        fields = ['url','discovery','detail','profit','material','workmanship','overheads','tender','year','note']

class AnalysisDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AnalysisDetail
        fields = ['url','analysis','category','definition','amount','price','total']

class ProgressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Progress
        fields = ['url','worksite','employer','subcontractor','no','date','cumulative','acquisition','additional','total','previous_amount','this_amount','vat','progress_amount','total_warrant','previous_warrant','this_warrant','total_advance','previous_advance','this_advance','total_stoppage','previous_stoppage','this_stoppage','total_tax_cut','previous_tax_cut','this_tax_cut','total_penalty','previous_penalty','this_penalty','total_deduction','previous_deduction','this_deduction','amount_paid']

class SynopsisSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Synopsis
        fields = ['url','progress','pose_no','name','unit','unit_price','total_quantity','previous_quantity','this_quantity','total_price','previous_price','this_price']