from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class users(models.Model):
    userid=models.CharField(primary_key=True,max_length=10)
    name=models.CharField(max_length=50)
    pswd=models.CharField(max_length=10)
    mobile = models.IntegerField(validators=[MinValueValidator(6000000000),MaxValueValidator(9999999999)])

    def __str__(self):
        return self.userid
    
    class Meta:
        verbose_name_plural='Users'

class JobDetails(models.Model):
    jobid=models.CharField(primary_key=True, max_length=10)
    userid = models.ForeignKey(users, on_delete=models.CASCADE)
    position=models.CharField(max_length=20)
    companyname=models.CharField(max_length=20)
    prerequisites=models.CharField(max_length=50,null=True)
    details=models.CharField(max_length=250,null=True)

    def __str__(self):
        return self.jobid
    
    class Meta:
        verbose_name_plural='Job Details'

class session(models.Model):
    userid=models.ForeignKey(users, on_delete=models.CASCADE)
    last_activity=models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(primary_key=True,max_length=30)

    def __str__(self):
        return self.userid_id
    
    class Meta:
        verbose_name_plural = 'Session'        
    





