from rest_framework import serializers
from courtzapi.models import RepFirm
# from courtzapi.serializers import FilerSerializer
from courtzapi.serializers import FilerSerializer
from courtzapi.serializers import FirmSerializer

class RepFirmSerializer(serializers.ModelSerializer):
    representative = FilerSerializer()
    firm = FirmSerializer()
    class Meta:
        model = RepFirm
        fields = ('id', 'representative', 'firm')