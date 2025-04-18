from rest_framework import serializers
from attendance.models import Attendance
from classes.serializers import FitnessClassSerializer, ClassBookingSerializer
from accounts.models import CustomUser
from classes.models import FitnessClass, ClassBooking

class AttendanceSerializer(serializers.ModelSerializer):
    fitness_class = FitnessClassSerializer(read_only=True)
    class_booking = ClassBookingSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'user', 'fitness_class', 'class_booking', 'attendance_date' , 'status']

    def create(self, validated_data):
        user = validated_data.get('user')

        # Automatically fetch the latest class booking for the user
        class_booking = ClassBooking.objects.filter(user=user).order_by('-id').first()
        if not class_booking:
            raise serializers.ValidationError("This user has no class bookings.")

        # Set the fitness class and attendance date based on the class booking
        validated_data['class_booking'] = class_booking
        validated_data['fitness_class'] = class_booking.fitness_class
        validated_data['attendance_date'] = class_booking.booking_date

        return super().create(validated_data)