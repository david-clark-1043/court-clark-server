from rest_framework import serializers
from django.contrib.auth.models import User

from courtzapi.models import Docket
from courtzapi.models import Filing
from courtzapi.models import Filer
from courtzapi.serializers import CaseStatusSerializer
# from courtzapi.serializers.docket_party_serializer import DocketPartySerializer
from courtzapi.serializers.filer_serializer import FilerSerializer, UserSerializer
from courtzapi.serializers.filing_type_serializer import FilingTypeSerializer

class DocketUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email',
                  'is_active', 'date_joined')

class DocketFilerSerializer(serializers.ModelSerializer):
    user = DocketUserSerializer()
    class Meta:
        model = Filer
        fields = ('id', 'user')

class DocketFilingSerializer(serializers.ModelSerializer):
    filing_type = FilingTypeSerializer()
    # filer = DocketFilerSerializer()
    class Meta:
        model = Filing
        fields = ('id', 'docket_party', 'title', 'docket_index', 'filed_on',
                  'filing_type', 'file_pdf')
        depth = 5

class DocketSerializer(serializers.ModelSerializer):
    status = CaseStatusSerializer()
    managers = FilerSerializer(many=True)
    filings = DocketFilingSerializer(many=True)
    # parties = DocketFilerSerializer(many=True)
    class Meta:
        model = Docket
        fields = ("id", "case_num", 'case_name', "status",
                  "created_on", "closed_on", 'managers', "docket_parties", "filings")
        depth = 4
