from datetime import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from rest_framework.decorators import action

from courtzapi.models import Docket, CaseStatus
from courtzapi.models.docket_parties import DocketParty
from courtzapi.models.filers import Filer
from courtzapi.models.firms import Firm
from courtzapi.models.party_type import PartyType
from courtzapi.models.rep__firm_parties import RepFirmParty
from courtzapi.models.rep_firms import RepFirm
from courtzapi.serializers import DocketSerializer

class DocketView(ViewSet):
    def list(self, request):
        """
        GET a list of dockets
        """
        filter_filer = request.query_params.get('filer', None)
        filter_open = request.query_params.get('open', None)
        filter_case_num = request.query_params.get('num', None)
        dockets = None
        
        if filter_filer is not None:
            filer = Filer.objects.get(pk=filter_filer)
            filer_type = filer.filer_type
            # filer_is_admin = filer.user.is_staff
            # if filer_is_admin:
            #     dockets = dockets.filter(managers=filer)
            # else:
            try:
                # TODO:
                # this now needs to be rep_firm_parties
                # search over both as rep and as party
                if filer_type.filer_type == "attorney":
                    dockets = Docket.objects.filter(docket_parties__rep_firm_party__party=filer)
                else:
                    dockets = Docket.objects.filter(docket_parties__rep_firm_party__rep_firm__representative=filer)
            except:
                pass
                
        if filter_open is not None:
            if dockets is not None:
                dockets = dockets.filter(status_id=1)
            else:
                dockets = Docket.objects.filter(status_id=1)
                
        if filter_case_num is not None:
            if dockets is not None:
                dockets = dockets.filter(case_num__contains=filter_case_num)
            else:
                dockets = Docket.objects.filter(case_num__contains=filter_case_num)
        
        if dockets is None:
            dockets = Docket.objects.all()
        
        serializer = DocketSerializer(dockets, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        """GET single docket"""
        docket = Docket.objects.get(pk=pk)
        serializer = DocketSerializer(docket)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['put'], detail=True)
    def close(self, request, pk):
        """ PUT method to close case """
        docket = Docket.objects.get(pk=pk)
        docket.status_id = 2
        docket.closed_on = datetime.now()
        docket.save()
        return Response(None, status=status.HTTP_200_OK)
        
    
    # @action(methods=['put'], detail=True)
    # def assignManager(self, request, pk):
    #     """ PUT method to assign managers to a docket """
    #     docket = Docket.objects.get(pk=pk)
    #     manager = Filer.objects.get(pk=request.data['manager_id'])
    #     docket.managers.add(manager)
    #     return Response({'message': 'Manager Added'}, status=status.HTTP_201_CREATED)
    
    # @action(methods=['put'], detail=True)
    # def unassignManager(self, request, pk):
    #     """ DELETE method to remove assigned managers from a docket """
    #     docket = Docket.objects.get(pk=pk)
    #     manager = Filer.objects.get(pk=request.data['manager_id'])
    #     docket.managers.remove(manager)
    #     return Response({'message': 'Manager Removed'}, status=status.HTTP_201_CREATED)

    @action(methods=['put'], detail=True)
    def assignParty(self, request, pk):
        """ PUT method to assign parties to a docket"""
        docket = Docket.objects.get(pk=pk)
        filer = Filer.objects.get(pk=request.data['filer_id'])
        filer_type = filer.filer_type
        party_type = PartyType.objects.get(pk=request.data['party_type_id'])
        filer_status = request.data['pro_se_status']
        if filer_type.filer_type == "judge":
            # add generic pro se relation
            # get judge firm object id is 4
            judge_firm = Firm.objects.get(pk=4)
            # check if filer-judge rep_firm exists
            rep_firm_exists = judge_firm in filer.firms.all()
            if not rep_firm_exists:
                filer.firms.add(judge_firm)
            
            # get rep_firm for rep_firm_party checks
            rep_firm = RepFirm.objects.get(representative=filer, firm=judge_firm)
            # check if rep_firm_party exists
            rep_firm_party_exists = rep_firm in filer.representation.all()
            if not rep_firm_party_exists:
                filer.representation.add(rep_firm)
            
            rep_firm_party = RepFirmParty.objects.get(rep_firm=rep_firm, party=filer)
        elif filer_type.filer_type == "clerk":
            # add generic pro se relation
            # get clerk firm object id is 5
            clerk_firm = Firm.objects.get(pk=5)
            # check if filer-clerk rep_firm exists
            rep_firm_exists = clerk_firm in filer.firms.all()
            if not rep_firm_exists:
                filer.firms.add(clerk_firm)
            
            # get rep_firm for rep_firm_party checks
            rep_firm = RepFirm.objects.get(representative=filer, firm=clerk_firm)
            # check if rep_firm_party exists
            rep_firm_party_exists = rep_firm in filer.representation.all()
            if not rep_firm_party_exists:
                filer.representation.add(rep_firm)
            
            rep_firm_party = RepFirmParty.objects.get(rep_firm=rep_firm, party=filer)
            
        elif filer_type.filer_type == "party" or filer_status:
            # add generic pro se relation
            # get pro se firm object id is 3
            pro_se_firm = Firm.objects.get(pk=3)
            # check if filer-pro se rep_firm exists
            rep_firm_exists = pro_se_firm in filer.firms.all()
            if not rep_firm_exists:
                filer.firms.add(pro_se_firm)
            
            # get rep_firm for rep_firm_party checks
            rep_firm = RepFirm.objects.get(representative=filer, firm=pro_se_firm)
            # check if rep_firm_party exists
            rep_firm_party_exists = rep_firm in filer.representation.all()
            if not rep_firm_party_exists:
                filer.representation.add(rep_firm)
            
            rep_firm_party = RepFirmParty.objects.get(rep_firm=rep_firm, party=filer)
            pass
        elif filer_type.filer_type == "attorney":
            # check if rep_firm exists
            firm = Firm.objects.get(pk=request.data["firm_id"])
            filer = Filer.objects.get(pk=request.data["filer_id"])
            party = Filer.objects.get(pk=request.data["party_id"])
            rep_firm_check = firm in filer.firms.all()
            if not rep_firm_check:
                filer.firms.add(firm)
            
            rep_firm = RepFirm.objects.get(firm=firm, representative=filer)
            # check if rep_firm_party exists
            rep_firm_party_check = rep_firm in party.representation.all()
            if not rep_firm_party_check:
                party.representation.add(rep_firm)
                
            rep_firm_party = RepFirmParty.objects.get(rep_firm=rep_firm, party=party)
            
            pass
        
        docket_party = DocketParty.objects.create(
            docket=docket,
            rep_firm_party=rep_firm_party,
            party_type=party_type
        )
        return Response({'message': "party added"}, status=status.HTTP_201_CREATED)
    
    @action(methods=['put'], detail=True)
    def unassignParty(self, request, pk):
        """ PUT method to assign parties to a docket"""
        docket = Docket.objects.get(pk=pk)
        rep_firm_party = RepFirmParty.objects.get(pk=request.data['rep_firm_party_id'])
        docket_parties = DocketParty.objects.filter(docket=docket, rep_firm_party=rep_firm_party)
        
        for docket_party in docket_parties:
            docket_party.delete()
        
        return Response({'message': "party deleted"}, status=status.HTTP_201_CREATED)
    
