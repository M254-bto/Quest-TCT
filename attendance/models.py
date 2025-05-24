from django.db import models
from django.utils.timezone import now
from datetime import date
from dateutil import relativedelta

# Create your models here.
from django.db import models

class Child(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    parent_name = models.CharField(max_length=100, blank=True, null=True)
    parent_contacts = models.CharField(max_length=100, blank=True, null=True)
    residence = models.CharField(max_length=100, blank=True, null=True)
    room = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Child'
        verbose_name_plural = 'Children'

    def __str__(self):
        return self.name

    def calculate_age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    def assign_room(self, age):
        if age is None:
            return None
        if age < 6:
            return "Kiota"
        elif age <= 11:
            return "Jasiri"
        return "Guza"

    def save(self, *args, **kwargs):
        if self.date_of_birth:
            self.age = self.calculate_age()
            self.room = self.assign_room(self.age)
        super().save(*args, **kwargs)
   
    # def save(self, *args, **kwargs):
    #     """Override save to auto-calculate age and room"""
    #     # Calculate age from date of birth
    #     self.age = self.age()
        
    #     # Determine room based on age
    #     self.room = self.room(self.age)
        
    #     super().save(*args, **kwargs)


class Attendance(models.Model):
    child = models.ForeignKey('Child', on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(default=now)
    check_out_time = models.DateTimeField(null=True, blank=True)
    card_number = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return f"{self.child.name} - {self.card_number}"