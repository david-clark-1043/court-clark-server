from django.db import models

class Filing(models.Model):
    filer = models.ForeignKey("Filer", on_delete=models.CASCADE)
    docket = models.ForeignKey("Docket", on_delete=models.CASCADE)
    docket_index = models.IntegerField()
    filed_on = models.DateTimeField(auto_now_add=True)
    filing_type = models.ForeignKey("FilingType", on_delete=models.CASCADE)
    filer_url = models.CharField(max_length=100)
