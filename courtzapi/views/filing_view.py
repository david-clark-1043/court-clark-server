import base64
import uuid
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile

from courtzapi.models import Filing, FilerType, RepFirm, PartyType
from courtzapi.models.case_status import CaseStatus
from courtzapi.models.docket_parties import DocketParty
from courtzapi.models.dockets import Docket
from courtzapi.models.filers import Filer
from courtzapi.models.filing_type import FilingType
from courtzapi.models.firms import Firm
from courtzapi.models.rep__firm_parties import RepFirmParty
from courtzapi.serializers import FilingSerializer

class FilingView(ViewSet):
    def list(self, request):
        """ GET list of filings """
        return ""
    
    def retrieve(self, request, pk):
        """GET single filing"""
        filing = Filing.objects.get(pk=pk)
        serializer = FilingSerializer(filing)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """ POST single filing """
        """ data needed in request
        # filer comes from the request token
        # docket_index generated from length of docket
        # in body of request
            # docket_id - if blank, make new docket
            # filing_type_id
            # file_url
        """
        
        # needs to check if the filing is a new docket
        new_docket = not request.data["docket_id"]
        
        if new_docket:
            count_as_string = f"{len(Docket.objects.all() + 1)}" # get num of dockets
            padding_needed = (8 - len(count_as_string)) * "0"
            case_num_padded = f"A-{padding_needed}{count_as_string}" # add padding up to 8 digits
            new_status = CaseStatus.objects.get(pk=1) # status = open (1)
            created_docket = Docket.objects.create( case_num = case_num_padded,
                                                    status = new_status)
            docket = Docket.objects.last()
        else: # or if the filing should use existing docket
            docket = Docket.objects.get(pk=request.data["docket_id"])
        
        # get filer object of the person submitting the filing
        filer = Filer.objects.get(pk=request.auth.user.id)

        # check if the filer is a judge, clerk, attorney, or party
        # this is for adding the correct RepFirmParty relationship
        filer_type = FilerType.objects.get(pk=filer.filer_type_id)
        filer_type = filer_type.filer_type
        filing_status = request.data["pro_se_status"]
        if filer_type == "judge":
            # add generic judge relation
            # check if filer-judge rep_firm exists
            
            # if rep_firm exists, use
            # if rep_firm not exists, create
            pass
        elif filer_type == "clerk":
            # add generic clerk relation
            # check if filer-clerk rep_firm exists
            
            # if rep_firm exists, use
            # if rep_firm not exists, create
            pass
        elif filer_type == "party" or filing_status:
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
        elif filer_type == "attorney":
            # add computed RepFirmParty
            # needs the party info, attorney info, and firm info?
            pass
        else:
            return Response({"message": "filer type error"})
        
        # get party type from request
        party_type = PartyType.objects.get(pk=request.data["party_type_id"])
        # check if RepFirmParty is associated with this docket
        try:
            docket_party = DocketParty.objects.get(
                rep_firm_party=rep_firm_party, 
                docket=docket, 
                party_type=party_type
            )
        except:
        # if it is not
            # create new DocketParty linking docket to the RepFirmParty
            docket_party = DocketParty.objects.create(
                rep_firm_party=rep_firm_party,
                docket=docket,
                party_type=party_type
            )
        # if it is, use existing DocketParty for the filing
        
        filing_type= FilingType.objects.get(pk=request.data['filing_type_id'])
        docket_index = len(docket.filings.all()) + 1

        # handle filing's file data
        filer_format, pdfstr = request.data["file_pdf"].split(';base64,')
        ext = filer_format.split('/')[-1]
        data = ContentFile(base64.b64decode(pdfstr), name=f'{request.data["title"]}.{ext}')

        new_filing = Filing.objects.create(
            docket_party=docket_party,
            docket=docket,
            docket_index=docket_index,
            filing_type=filing_type,
            title=request.data['title'],
            file_pdf = data
        )
        serializer = FilingSerializer(new_filing)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk):
        """ DELETE single filing """
        return ""

    # currently not allowing filing updates
    # misfiled items should be amended using a new filing    
    # def update(self):
    #     return ""