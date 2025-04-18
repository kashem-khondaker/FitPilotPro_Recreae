from rest_framework import serializers
from payments.models import Payment
from memberships.models import  MembershipPlan
from memberships.serializers import MembershipPlanSerializer , MembershipSerializer


class SimpleMembershipPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPlan
        fields = [ 'name', 'description', 'price', 'duration_in_days']

class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    membership_plan = serializers.PrimaryKeyRelatedField(queryset=MembershipPlan.objects.all(), write_only=True)
    membership = MembershipSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'membership', 'membership_plan', 'amount', 'payment_date', 'payment_method', 'transaction_id']
        read_only_fields = [ 'user', 'payment_date' , 'amount' , 'transaction_id']

    def create(self, validated_data):
        membership_plan = validated_data.get('membership_plan')
        if membership_plan:
            validated_data['amount'] = membership_plan.price
        return super().create(validated_data)