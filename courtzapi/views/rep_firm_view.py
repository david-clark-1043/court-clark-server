from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from courtzapi.models import Filer, RepFirm
from courtzapi.serializers import RepFirmSerializer
class RepFirmView(ViewSet):
    def list(self, request):
        """ GET requests for repFirms """
        
        rep_filter = request.query_params.get('filer', None)
        rep_firms = RepFirm.objects.all()
        
        if rep_filter is not None:
            rep = Filer.objects.get(pk=rep_filter)
            rep_firms = rep_firms.filter(representative=rep)
            
        serializer = RepFirmSerializer(rep_firms, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request):
        return ""