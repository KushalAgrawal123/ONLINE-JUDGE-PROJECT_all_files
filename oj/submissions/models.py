from django.db import models
from django.conf import settings
from problems.models import Problem

class Submission(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    problem=models.ForeignKey(Problem,on_delete=models.CASCADE)
    code=models.TextField(); language=models.CharField(max_length=30)
    verdict=models.CharField(max_length=20,default='Pending')
    submitted_at=models.DateTimeField(auto_now_add=True)