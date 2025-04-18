from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from payments.models import Payment
from payments.serializers import PaymentSerializer
from core.permissions import IsMemberOrAdminStaff, IsAdminOrStaff
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from memberships.models import Membership, MembershipPlan
from core.permissions import PaymentPermissions
from core.filters import PaymentFilter
from datetime import timedelta
from django.db import transaction

class PaymentPagination(PageNumberPagination):
    page_size = 15

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('user', 'membership', 'membership_plan').all()
    serializer_class = PaymentSerializer
    permission_classes = [PaymentPermissions]
    pagination_class = PaymentPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['amount', 'payment_date', 'payment_method', 'user__email']
    search_fields = ['transaction_id', 'user__email', 'membership_plan__name']
    ordering_fields = ['amount', 'payment_date']
    filterset_class = PaymentFilter

    def get_queryset(self):
        try:
            if getattr(self, 'swagger_fake_view', False):
                return Payment.objects.none()
            
            user = self.request.user
            if not user.is_authenticated:
                return Payment.objects.none()
            if user.is_superuser or user.role in ['ADMIN', 'STAFF']:
                return Payment.objects.select_related('user', 'membership', 'membership_plan').all()
            elif user.role == 'MEMBER':
                return Payment.objects.filter(user=user).select_related('user', 'membership', 'membership_plan')
            return Payment.objects.none()
        except Exception as e:
            raise ValidationError({'error': str(e)})

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of payments",
        responses={200: PaymentSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('amount_min', openapi.IN_QUERY, description="Minimum amount", type=openapi.TYPE_NUMBER),
            openapi.Parameter('amount_max', openapi.IN_QUERY, description="Maximum amount", type=openapi.TYPE_NUMBER),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new payment",
        request_body=PaymentSerializer,
        responses={201: PaymentSerializer, 400: "Bad Request"}
    )
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        membership_plan_id = data.get('membership_plan')
        membership_id = data.get('membership')

        try:
            with transaction.atomic():
                if membership_plan_id:
                    plan = MembershipPlan.objects.get(id=membership_plan_id)
                    data['amount'] = plan.price
                elif membership_id:
                    membership = Membership.objects.select_related('plan').get(id=membership_id)
                    data['amount'] = membership.plan.price
                else:
                    return Response({"error": "Membership or MembershipPlan is required"}, status=400)

                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)

                # Automatically create Membership
                payment_instance = serializer.instance
                payment_instance.is_successful = True
                payment_instance.save()

                if membership_plan_id:
                    membership = Membership.objects.create(
                        user=payment_instance.user,
                        plan=plan,
                        start_date=payment_instance.payment_date,
                        end_date=payment_instance.payment_date + timedelta(days=plan.duration_in_days),
                        is_active=True
                    )
                    payment_instance.membership = membership
                    payment_instance.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific payment",
        responses={200: PaymentSerializer, 404: "Not Found"}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update details of a specific payment",
        request_body=PaymentSerializer,
        responses={200: PaymentSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update details of a specific payment",
        request_body=PaymentSerializer,
        responses={200: PaymentSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific payment",
        responses={204: "No Content", 404: "Not Found"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrStaff])
    def payment_report(self, request):
        try:
            if request.user.role == 'ADMIN':
                payment_data = Payment.objects.select_related('user', 'membership_plan').all()
                serializer = self.get_serializer(payment_data, many=True)
                return Response(serializer.data)
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
