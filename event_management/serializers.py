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
            # assignment_data['task'] = task  # Automatically associate the created task
            assignment_data.pop('task', None)
            Assignment.objects.create(task=task, **assignment_data)

            # Assignment.objects.create(**assignment_data)
        return task
    def update(self, instance, validated_data):
        # Extract and update assignments
        assignments_data = validated_data.pop('assignments', [])
        
        # Update the task fields
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.event = validated_data.get('event', instance.event)
        instance.save()

        # Update or create assignment objects
        for assignment_data in assignments_data:
            assignment_data.pop('task', None)
            assignment_instance = instance.assignments.filter(id=assignment_data.get('id')).first()
            if assignment_instance:
                # If the assignment exists, update it
                for attr, value in assignment_data.items():
                    setattr(assignment_instance, attr, value)
                assignment_instance.save()
            else:
                # If the assignment doesn't exist, create a new one
                Assignment.objects.create(task=instance, **assignment_data)

        return instance