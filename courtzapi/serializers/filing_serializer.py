from rest_framework import serializers
from courtzapi.models import Filing
from courtzapi.models.dockets import Docket
from courtzapi.serializers import FilerSerializer
from courtzapi.serializers import FilingTypeSerializer
from courtzapi.serializers import CaseStatusSerializer
from courtzapi.serializers import DocketSerializer

class FilingDocketSerializer(serializers.ModelSerializer):
    status = CaseStatusSerializer()
    class Meta:
        model = Docket
        fields = ("id", "case_num", 'case_name', "status",
                  "created_on", "closed_on")
        depth = 2

class FilingSerializer(serializers.ModelSerializer):
    # filer = FilerSerializer()
    docket = FilingDocketSerializer()
    filing_type = FilingTypeSerializer()
    class Meta:
        model = Filing
        fields = ('id', 'docket_party', 'title', 'docket', 'docket_index',
                  'filed_on', 'filing_type', 'file_pdf')
        depth = 5