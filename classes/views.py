from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from classes.models import FitnessClass, ClassBooking
from classes.serializers import FitnessClassSerializer, ClassBookingSerializer
from core.permissions import IsAdminOrStaffOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters import rest_framework as filters
from core.filters import FitnessClassFilter
from core.permissions import IsMemberOrAdminStaff
from rest_framework.decorators import action
from core.permissions import IsAdminOrStaff
from rest_framework.permissions import IsAuthenticated

# Create your views here.



class FitnessClassPagination(PageNumberPagination):
    page_size = 12

class ClassBookingPagination(PageNumberPagination):
    page_size = 6

class FitnessClassViewSet(viewsets.ModelViewSet):
    """ 
    Fitness classes overview:
    for create -
        . Only admin and staff can create, update, and delete classes.
        . All users can view classes.
    features:
        . Filter by instructor email and max capacity.
        . Search by name, description, and instructor email.
        . Paginate results.
    """
    queryset = FitnessClass.objects.select_related('instructor').all()
    serializer_class = FitnessClassSerializer
    permission_classes = [IsAdminOrStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FitnessClassFilter
    search_fields = ['name', 'description', 'instructor__email']
    ordering_fields = ['schedule', 'max_capacity']
    pagination_class = FitnessClassPagination

    def get_queryset(self):
        # Handle Swagger schema generation
        if getattr(self, 'swagger_fake_view', False):
            return FitnessClass.objects.none()

        user = self.request.user
        if not user.is_authenticated:
            return FitnessClass.objects.select_related('instructor').all()

        if user.is_superuser or user.role == 'ADMIN':
            return FitnessClass.objects.select_related('instructor').all()
        elif user.role == 'STAFF':
            return FitnessClass.objects.select_related('instructor').all()
        
        return FitnessClass.objects.select_related('instructor').all()
    
    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of fitness classes.\n\nEvery user can filter by instructor email and max capacity, and search by name, description, and instructor email.\n\nPermissions:\n1. All users can access this endpoint.\n2. Superuser and staff can create, update, and delete classes.\n3. Members can only view classes.",
        responses={
            200: FitnessClassSerializer(many=True),
            403: "Forbidden",
        },
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('instructor__email', openapi.IN_QUERY, description="Filter by instructor email", type=openapi.TYPE_STRING),
            openapi.Parameter('max_capacity', openapi.IN_QUERY, description="Filter by max capacity", type=openapi.TYPE_INTEGER),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by name, description, or instructor email", type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Create a new fitness class",
        request_body= FitnessClassSerializer,
        responses={
            201: FitnessClassSerializer,
            400: "Bad Request",
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific fitness class",
        responses={
            200: FitnessClassSerializer,
            404: "Not Found",
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update details of a specific fitness class",
        request_body=FitnessClassSerializer,
        responses={
            200: FitnessClassSerializer,
            400: "Bad Request",
            404: "Not Found",
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update details of a specific fitness class",
        request_body=FitnessClassSerializer,
        responses={
            200: FitnessClassSerializer,
            400: "Bad Request",
            404: "Not Found",
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific fitness class",
        responses={
            204: "No Content",
            404: "Not Found",
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrStaff])
    def class_report(self, request):
        try:
            if request.user.role == 'ADMIN' or request.user.is_superuser:
                # Generate class report
                class_data = FitnessClass.objects.select_related('instructor').all()
                serializer = FitnessClassSerializer(class_data, many=True)
                return Response(serializer.data)
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClassBookingViewSet(viewsets.ModelViewSet):
    
    serializer_class = ClassBookingSerializer
    permission_classes = [IsMemberOrAdminStaff]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['fitness_class__name', 'user__email']
    search_fields = ['fitness_class__name', 'user__email']
    ordering_fields = ['booking_date']
    pagination_class = ClassBookingPagination

    def get_queryset(self):
        user = self.request.user

        if getattr(self, 'swagger_fake_view', False):
            return ClassBooking.objects.none()
        
        if user.is_superuser or user.role == 'ADMIN':
            return ClassBooking.objects.select_related('user', 'fitness_class').all()
        elif user.role == 'STAFF':
            return ClassBooking.objects.select_related('user', 'fitness_class').all()
        elif user.role == 'MEMBER':
            return ClassBooking.objects.filter(user=user).select_related('user', 'fitness_class')
        
        return ClassBooking.objects.none()

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific class booking",
        responses={
            200: ClassBookingSerializer,
            404: "Not Found",
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update details of a specific class booking",
        request_body=ClassBookingSerializer,
        responses={
            200: ClassBookingSerializer,
            400: "Bad Request",
            404: "Not Found",
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update details of a specific class booking",
        request_body=ClassBookingSerializer,
        responses={
            200: ClassBookingSerializer,
            400: "Bad Request",
            404: "Not Found",
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific class booking",
        responses={
            204: "No Content",
            404: "Not Found",
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=False , methods=['get'] , permission_classes=[IsAdminOrStaff])
    def class_booking_report(self , request):
        try:
            if request.user.role in ['ADMIN' , 'STAFF'] or request.user.is_superuser:
                # Generate class booking report
                booking_data = ClassBooking.objects.select_related('user' , 'fitness_class').all()
                serializer = ClassBookingSerializer(booking_data , many=True)
                return Response(serializer.data)
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)