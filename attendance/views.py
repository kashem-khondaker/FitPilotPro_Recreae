from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from core.permissions import IsAdminOrStaff
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class AttendancePagination(PageNumberPagination):
    page_size = 20

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('user', 'fitness_class', 'class_booking').all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    pagination_class = AttendancePagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['fitness_class__name', 'user__email', 'attendance_date']

    def get_queryset(self):
        user = self.request.user

        # Handle schema generation or unauthenticated users
        if getattr(self, 'swagger_fake_view', False) or not user.is_authenticated:
            return Attendance.objects.none()

        if user.is_superuser or user.role == 'ADMIN':
            return Attendance.objects.select_related('user', 'fitness_class', 'class_booking').all()
        elif user.role == 'STAFF':
            return Attendance.objects.select_related('user', 'fitness_class', 'class_booking').all()
        # Restrict MEMBER role to only see their own attendance
        return Attendance.objects.filter(user=user).select_related('user', 'fitness_class', 'class_booking')

    @swagger_auto_schema(
        operation_description="Retrieve all attendances",
        responses={
            200: AttendanceSerializer(many=True),
            403: "Forbidden",
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new payment",
        request_body=AttendanceSerializer,
        responses={
            201: AttendanceSerializer,
            400: "Bad Request",
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    

    # @action(detail=False, methods=['post'], permission_classes=[IsAdminOrStaff])
    # def mark_attendance(self, request):
    #     """Allow staff to mark attendance for members."""
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrStaff])
    def attendance_report(self, request):
        """Generate attendance reports for admins."""
        attendance_data = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(attendance_data, many=True)
        return Response(serializer.data)