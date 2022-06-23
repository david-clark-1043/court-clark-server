from django.db import models

class Docket(models.Model):
    case_num = models.CharField(max_length=50, null=True)
    case_name = models.CharField(max_length=300, null=True)
    status = models.ForeignKey("CaseStatus", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    closed_on = models.DateTimeField(null=True, blank=True)

    @property
    def managers(self):
        docket_parties = self.docket_parties.all()
        manager_list = []
        for docket_party in docket_parties:
            rep_firm_party = docket_party.rep_firm_party
            rep_firm = rep_firm_party.rep_firm
            firm = rep_firm.firm
            if firm.name == "judge" or firm.name == "clerk":
                manager_list.append(rep_firm.representative)
        return manager_list

    # @managers.setter
    # def managers(self, value):
    #     self.__joined = value