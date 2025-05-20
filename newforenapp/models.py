from django.db import models
from django.utils import timezone

# Create your models here.

class Report(models.Model):
    uuid = models.CharField(max_length=200, unique=True)  
    number = models.CharField(max_length=255) 
    currentDate = models.TextField()  
    reportDate = models.TextField()  
    documentOutDetails = models.TextField( )  
    requestedInformation = models.TextField(verbose_name="المعلومات المطلوبة")
    conclusion = models.TextField() 
    userId = models.TextField( null=True, blank=True)  
    status = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report {self.uuid} - {self.number}"

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
class CommitteeMember(models.Model):
    uuid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=500)
    position = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=100, default='local')
    section_id = models.TextField()
    section_uuid = models.CharField(null=True, blank=True , max_length=255)
    userId = models.IntegerField()
    rank = models.TextField(null=True, blank=True)
    isHidden = models.TextField(default=False , null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
