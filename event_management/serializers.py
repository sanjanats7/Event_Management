from rest_framework import serializers
from .models import Event, Attendee, Task, Assignment

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    attendee = serializers.PrimaryKeyRelatedField(queryset=Attendee.objects.all())
    
    class Meta:
        model = Assignment
        fields = ['event', 'task', 'attendee']
        
class TaskSerializer(serializers.ModelSerializer):
    assignments = AssignmentSerializer(many=True)  # This will serialize the related assignments
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'event','assignments']
    def create(self, validated_data):
        assignments_data = validated_data.pop('assignments', [])
        task = Task.objects.create(**validated_data)
        for assignment_data in assignments_data:
            assignment_data['task'] = task  # Automatically associate the created task
            Assignment.objects.create(**assignment_data)
        return task