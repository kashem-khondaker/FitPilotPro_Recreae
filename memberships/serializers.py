from rest_framework import serializers
from memberships.models import MembershipPlan, Membership
from accounts.models import CustomUser

class MembershipPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPlan
        fields = ['id', 'name', 'description', 'price', 'duration_in_days', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class MembershipSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    plan = serializers.PrimaryKeyRelatedField(queryset=MembershipPlan.objects.all())
    plan_detail = MembershipPlanSerializer(source='plan', read_only=True)

    class Meta:
        model = Membership
        fields = ['id', 'user', 'plan', 'plan_detail' , 'start_date', 'end_date', 'is_active']
        # read_only_fields = ['start_date', 'end_date']