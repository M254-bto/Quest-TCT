from rest_framework import viewsets
from .models import Child
from .serializers import ChildSerializer
from django.http import JsonResponse



class ChildViewSet(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer



def check_in(request, pk):
    child = Child.objects.get(pk=pk)
    child.attendance_set.create(check_in=True)
    return JsonResponse({'status': 'success'})


def check_out(request, pk):
    child = Child.objects.get(pk=pk)
    if child.check_out:
        return JsonResponse({'status': 'error', 'message': 'Already checked out'})
    if not child.check_in:
        return JsonResponse({'status': 'error', 'message': 'Not checked in'})