from django.db import models

class DocketParty(models.Model):
    rep_firm_party = models.ForeignKey("RepFirmParty", on_delete=models.CASCADE, related_name="docket_parties")
    docket = models.ForeignKey("Docket", on_delete=models.CASCADE, related_name="docket_parties")
    party_type = models.ForeignKey("PartyType", on_delete=models.CASCADE)
