from django.db import models
from django.utils.timezone import now

# Create your models here.
from django.db import models

class Child(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    parent_name = models.CharField(max_length=100, blank=True, null=True)   
    parent_contacts = models.CharField(max_length=100, blank=True, null=True)   
    residence = models.CharField(max_length=100, blank=True, null=True)
    room = models.CharField(max_length=100)

    class meta:
        verbose_name = 'Child'
        verbose_name_plural = 'Children'

    def __str__(self):
        return self.name



class Attendance(models.Model):
    child = models.ForeignKey('Child', on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(default=now)
    check_out_time = models.DateTimeField(null=True, blank=True)
    card_number = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return f"{self.child.name} - {self.card_number}"