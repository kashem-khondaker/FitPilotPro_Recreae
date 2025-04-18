from rest_framework import serializers
from classes.models import FitnessClass, ClassBooking
from accounts.models import CustomUser

class FitnessClassSerializer(serializers.ModelSerializer):
    instructor = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'description', 'image', 'duration', 'max_capacity', 'instructor', 'schedule', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        ref_name = 'ClassesFitnessClass'

class ClassBookingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    fitness_class = serializers.PrimaryKeyRelatedField(queryset=FitnessClass.objects.all())

    class Meta:
        model = ClassBooking
        fields = ['id', 'user', 'fitness_class', 'booking_date']
        read_only_fields = ['booking_date' , 'booking_date']