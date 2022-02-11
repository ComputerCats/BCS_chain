from django.db import models
import json

# Create your models here.


class Data_base_Transaction(models.Model):
    Txid = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return (self.Txid, self.description)
