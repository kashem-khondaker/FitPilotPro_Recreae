from rest_framework import serializers
from reports.models import Report
from accounts.serializers import UserSerializer
from classes.serializers import FitnessClassSerializer

class ReportSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    fitness_class = FitnessClassSerializer(read_only=True)

    class Meta:
        model = Report
        fields = ['id', 'user', 'fitness_class', 'report_date', 'content']