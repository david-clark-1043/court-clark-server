from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.auth.models import User
from courtzapi.models import Firm
from courtzapi.models.filers import Filer
from courtzapi.serializers import FirmSerializer


class FirmView(ViewSet):
    def list(self, request):
        """
        GET a list of possible case statuses
        """
        firms = Firm.objects.all()
        serializer = FirmSerializer(firms, many=True)
        return Response(serializer.data)
    
    @action(methods=['put'], detail=False)
    def addRelation(self, request):
        user = Filer.objects.get(pk=request.data['filer_id'])
        firm = Firm.objects.get(pk=request.data['firm_id'])
        user.firms.add(firm)
        return Response({'message': "firm added to user"}, status=status.HTTP_201_CREATED)
    
    @action(methods=['put'], detail=False)
    def removeRelation(self, request):
        user = Filer.objects.get(pk=request.data['filer_id'])
        firm = Firm.objects.get(pk=request.data['firm_id'])
        user.firms.remove(firm)
        return Response({'message': "firm removed from user"}, status=status.HTTP_204_NO_CONTENT)