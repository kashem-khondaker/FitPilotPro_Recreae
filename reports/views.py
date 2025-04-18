from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from core.permissions import IsAdminOrStaff

from accounts.models import CustomUser
from classes.models import FitnessClass
from feedback.models import Feedback
from memberships.models import Membership
from attendance.models import Attendance
from payments.models import Payment
from reports.models import Report

from accounts.serializers import UserSerializer
from classes.serializers import FitnessClassSerializer
from feedback.serializers import FeedbackSerializer
from memberships.serializers import MembershipSerializer
from attendance.serializers import AttendanceSerializer
from payments.serializers import PaymentSerializer
from reports.serializers import ReportSerializer

# Create your views here.

class ReportViewSet(viewsets.ModelViewSet):

    """
    Report Viewset to handle all reports related to the fitness application.
    This viewset provides endpoints for generating various reports such as:
    
    1. Membership Report: /reports/membership_report/
    2. Attendance Report: /reports/attendance_report/
    3. Feedback Report: /reports/feedback_report/
    4. User Report: /reports/user_report/
    5. Class Report: /reports/class_report/
    6. Payment Report: /reports/payment_report/
    
    """


    queryset = Report.objects.select_related('user', 'fitness_class').all()
    serializer_class = ReportSerializer
    permission_classes = [IsAdminOrStaff]


    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrStaff])
    def attendance_report(self, request):
        try:
            if request.user.role == 'ADMIN':
                # Generate attendance report
                attendance_data = Attendance.objects.select_related('user', 'fitness_class').all()
                serializer = AttendanceSerializer(attendance_data, many=True)
                return Response(serializer.data)
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrStaff])
    def user_report(self, request):
        try:
            if request.user.role == 'ADMIN':
                # Generate user report
                
                user_data = CustomUser.objects.all()
                serializer = UserSerializer(user_data, many=True)
                return Response(serializer.data)
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrStaff])
    def payment_report(self, request):
        try:
            if request.user.role == 'ADMIN':
                # Generate payment report
                
                payment_data = Payment.objects.select_related('user', 'membership_plan').all()
                serializer = PaymentSerializer(payment_data, many=True)
                return Response(serializer.data)
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)