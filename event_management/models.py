from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateField()

    def clean(self):
        if not self.name or not self.description or not self.location:
            raise ValidationError("All fields must be filled.")
          
    def __str__(self):
        return self.name

class Attendee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="Enter a valid email address.")]
    )
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\d{10,15}$', "Phone number must be between 10 and 15 digits.")]
    )

    def clean(self):
        if not self.name or not self.email or not self.phone_number:
            raise ValidationError("All fields must be filled.")
          
    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    event = models.ForeignKey(Event, related_name='tasks', on_delete=models.CASCADE)
    def clean(self):
        if not self.title or not self.description:
            raise ValidationError("Title and Description are required.")


    def __str__(self):
        return self.title

class Assignment(models.Model):
    event = models.ForeignKey(Event, related_name='assignments', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='assignments', on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee, related_name='assignments', on_delete=models.CASCADE)

    def clean(self):
        if not self.event or not self.task or not self.attendee:
            raise ValidationError("All fields must be filled.")
          
    def __str__(self):
        return f"{self.task.title} -> {self.attendee.name}"
      
class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # Store hashed password
    is_admin = models.BooleanField(default=False)