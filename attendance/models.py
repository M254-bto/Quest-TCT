from django.db import models

# Create your models here.
from django.db import models

class Child(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    parent_name = models.CharField(max_length=100)
    parent_contacts = models.CharField(max_length=100)
    residence = models.CharField(max_length=100)
    room = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    check_in = models.BooleanField()
    check_out = models.BooleanField()


    def __str__(self):
        return self.child.name