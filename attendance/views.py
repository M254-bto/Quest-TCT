from rest_framework import viewsets
from .models import Child, Attendance
from .serializers import ChildSerializer, AttendanceSerializer
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Q
from collections import defaultdict
from django.db.models import Count
from rest_framework.filters import SearchFilter



class PrefixSearchFilter(SearchFilter):
    def construct_search(self, search_fields):
        return f"{search_fields}__istartswith"


class ChildViewSet(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer



class SearchChildView(ListAPIView):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    filter_backends = [PrefixSearchFilter]
    search_fields = ['name']


# def check_in(request, pk):
#     child = Child.objects.get(pk=pk)
#     if child.check_in:
#         return JsonResponse({'status': 'error', 'message': 'Already checked in'})
#     if child.check_out:
#         return JsonResponse({'status': 'error', 'message': 'Already checked out'})
#     child.check_in = True
#     child.save()
#     return JsonResponse({'status': 'success'})

class CheckInView(APIView):
    def post(self, request):
        child_id = request.data.get('child_id')
        card_number = request.data.get('card_number')
        print(child_id, card_number)
        
        # Check if the child exists
        try:
            child = Child.objects.get(id=child_id)
            print(child)
        except Child.DoesNotExist:
            return Response({"error": "Child not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the child has already checked in today
        today = now().date()
        if Attendance.objects.filter(child=child, check_in_time__date=today).exists():
            return Response({"error": "Child already checked in today"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the card number is already in use
        if Attendance.objects.filter(card_number=card_number, check_in_time__date=today).exists():
            return Response({"error": "Card number already in use"}, status=status.HTTP_400_BAD_REQUEST)

        # Create attendance record
        attendance = Attendance.objects.create(child=child, card_number=card_number)
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
# def check_out(request, pk):
#     child = Child.objects.get(pk=pk)
#     if child.check_out:
#         return JsonResponse({'status': 'error', 'message': 'Already checked out'})
#     if not child.check_in:
#         return JsonResponse({'status': 'error', 'message': 'Not checked in'})
#     child.check_out = True
#     child.save()
#     return JsonResponse({'status': 'success'})


class CheckOutView(APIView):
    def post(self, request):
        card_number = request.data.get('card_number')
        print(card_number)

        # Find the attendance record by card number
        try:
            attendances = Attendance.objects.filter(card_number=card_number, check_out_time__isnull=True)
        except Attendance.DoesNotExist:
            return Response({"error": "Attendance record not found or already checked out"}, status=status.HTTP_404_NOT_FOUND)

        # Mark as checked out and set card number to empty
        for attendance in attendances:
            attendance.check_out_time = now()
            # attendance.card_number = ''
            attendance.card_number = ''
            attendance.save()
        return Response(
            {"message": f"Checked out {attendances.count()} record(s) successfully"},
            status=status.HTTP_200_OK
        )
    
        
    






#View for all chidren not checked out and return name and card number
class ChildrenNotCheckedOut(ListAPIView):
    """
    View to list all card numbers and corresponding child names
    where children have checked in but not checked out for the current date.
    """
    serializer_class = AttendanceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['child__name', 'card_number']

    def get_queryset(self):
        today = now().date()
        return Attendance.objects.filter(check_out_time__isnull=True, check_in_time__date=today)
    


class AttendanceCount(APIView):
    def get(self, request):
        today = now().date()
        total_children = Child.objects.count()
        checked_in_children = Attendance.objects.filter(check_in_time__date=today).count()
        checked_out_children = Attendance.objects.filter(check_out_time__date=today).count()
        return Response({
            "total_children": total_children,
            "checked_in_children": checked_in_children,
            "checked_out_children": checked_out_children
        })
    

class MonthlyAttendance(APIView):
    def get(self, request):
        # Get today's date
        today = now().date()

        # Calculate first and last day of this month
        first_day_this_month = today.replace(day=1)
        last_day_this_month = today

        # Calculate first and last day of last month
        first_day_last_month = (first_day_this_month - timedelta(days=1)).replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)

        # Determine which period to return based on query param
        period = request.query_params.get("period", "this_month")

        if period == "last_month":
            start_date, end_date = first_day_last_month, last_day_last_month
        else:  # Default to this month
            start_date, end_date = first_day_this_month, last_day_this_month

        # Filter attendance records for the selected period
        attendance_records = Attendance.objects.filter(check_in_time__date__range=[start_date, end_date])

        # Serialize the data
        serialized_data = AttendanceSerializer(attendance_records, many=True).data

        # Group by date
        grouped_attendance = defaultdict(list)
        for record in serialized_data:
            check_in_date = record["check_in_time"][:10]  # Extract YYYY-MM-DD
            grouped_attendance[check_in_date].append(record)

        return Response(grouped_attendance)