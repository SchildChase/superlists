from django.db import models

class List(models.Model):
    pass
class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.SET_DEFAULT,default='')

# Create your models here.
