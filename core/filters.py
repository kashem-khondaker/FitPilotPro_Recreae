from django_filters import rest_framework as filters
from memberships.models import MembershipPlan
from classes.models import FitnessClass
from payments.models import Payment

class FitnessClassFilter(filters.FilterSet):
    max_capacity_min = filters.NumberFilter(field_name="max_capacity", lookup_expr="gte")
    max_capacity_max = filters.NumberFilter(field_name="max_capacity", lookup_expr="lte")

    class Meta:
        model = FitnessClass
        fields = ['max_capacity_min', 'max_capacity_max', 'instructor__email']

class MembershipPlanFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = filters.NumberFilter(field_name="price", lookup_expr="lte")
    duration_min = filters.NumberFilter(field_name="duration_in_days", lookup_expr="gte")
    duration_max = filters.NumberFilter(field_name="duration_in_days", lookup_expr="lte")

    class Meta:
        model = MembershipPlan
        fields = ['price_min', 'price_max', 'duration_min', 'duration_max']


class PaymentFilter(filters.FilterSet):
    amount_min = filters.NumberFilter(field_name="amount", lookup_expr="gte")
    amount_max = filters.NumberFilter(field_name="amount", lookup_expr="lte")
    payment_date_min = filters.DateFilter(field_name="payment_date", lookup_expr="gte")
    payment_date_max = filters.DateFilter(field_name="payment_date", lookup_expr="lte")

    class Meta:
        model = Payment
        fields = ['amount_min', 'amount_max', 'payment_date_min', 'payment_date_max']