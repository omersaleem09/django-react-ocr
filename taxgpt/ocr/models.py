from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class ExtractedText(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    pdf_file = models.FileField(upload_to='uploads/')
    ssn = models.CharField(max_length=255, null=True, blank=True)
    ein = models.CharField(max_length=255, null=True, blank=True)
    f_name = models.CharField(max_length=255, null=True, blank=True)
    l_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    emp_name = models.CharField(max_length=255, null=True, blank=True)
    emp_last_name = models.CharField(max_length=255, null=True, blank=True)
    wtc_val = models.CharField(max_length=255, null=True, blank=True)
    fit_val = models.CharField(max_length=255, null=True, blank=True)
    ssw_val = models.CharField(max_length=255, null=True, blank=True)
    sst_val = models.CharField(max_length=255, null=True, blank=True)
    mwt_val = models.CharField(max_length=255, null=True, blank=True)
    mtw_val = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username


    

