from django.db import models


class Responses(models.Model):
    first_Name = models.CharField(max_length=50, blank=False)
    last_Name = models.CharField(max_length=50, blank=True, null=True)
    mobile_No = models.CharField(max_length=15, blank=False)
    email_Id = models.EmailField(max_length=254, blank=False)
    monthly_Saving = models.BigIntegerField(blank=False, default=0)
    monthly_Income = models.BigIntegerField(blank=False, default=0)
