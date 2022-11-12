from django.db import models


class MasterWordTable(models.Model):
    english = models.CharField(max_length=100)
    japanese = models.CharField(max_length=100)
    grade = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)