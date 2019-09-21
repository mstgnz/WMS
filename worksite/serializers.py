from rest_framework import serializers
from firm.models import Firm, Worksite, Subcontractor, Contract

class FirmSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Firm
        fields = ('url','tax','name','full_name','phone','fax','web','email','address','image')

class WorksiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Worksite
        fields = ('url','firm','name','employer','name_of_job','control','construction_area','threader_no','island_no','parcel_no','phone','fax','address','image','start_date','end_date','active')

class SubcontractorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subcontractor
        fields = ('url','firm','worksite','name','email','phone','subject','address')

class ContractSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contract
        fields = ('url','worksite','category','no','date','name','price','guarantee','advance','note','file')