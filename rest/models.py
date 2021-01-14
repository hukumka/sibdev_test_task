from django.db import models


class Deal(models.Model):
    customer = models.CharField(max_length=30)
    item = models.CharField(max_length=30)
    total = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField()
