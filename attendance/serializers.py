from rest_framework import serializers
from .models import Child, Attendance

class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'



class AttendanceSerializer(serializers.ModelSerializer):
    child_name = serializers.CharField(source='child.name', read_only=True)

    class Meta:
        model = Attendance
        fields = ['card_number', 'child_name', 'check_in_time', 'check_out_time']
