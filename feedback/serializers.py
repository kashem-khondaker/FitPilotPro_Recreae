from rest_framework import serializers
from feedback.models import Feedback
from classes.models import FitnessClass

class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'description', 'duration', 'instructor']
        ref_name = 'FeedbackFitnessClass'

class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    fitness_class = serializers.PrimaryKeyRelatedField(queryset=FitnessClass.objects.select_related('instructor').all() )
    rating = serializers.IntegerField(min_value=1, max_value=5)
    fitness_class_details = FitnessClassSerializer(source='fitness_class', read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'fitness_class', 'fitness_class_details', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']