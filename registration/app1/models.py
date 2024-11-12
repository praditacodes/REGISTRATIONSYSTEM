from django.db import models
from django.contrib.auth.models import User

class Record(models.Model):
    STATUS_CHOICES = [
        ('good', 'Good'),
        ('reconstruction', 'Reconstruction'),
    ]
    AI_CHOICES = [
        ('good', 'Good'),
        ('reconstruction', 'Reconstruction'),
    ]

    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='records', help_text="User associated with this record")

    
    serial_number = models.IntegerField(unique=True, help_text="Unique serial number for the record")

    image = models.ImageField(upload_to='images/', help_text="Upload an image for the record")

    
    enum_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='good', help_text="Status of the record")

    pin = models.BooleanField(default=False, help_text="Indicates whether a PIN is set for the record")

   
    ai_status = models.CharField(max_length=50, choices=AI_CHOICES, default='good', help_text="AI assessment status")

   
    comment = models.TextField(blank=True, null=True, help_text="Additional comments for the record")


    commit = models.BooleanField(default=False, help_text="Commit status of the record")

   
    status = models.CharField(max_length=50, blank=True, help_text="Additional status information")

    def __str__(self):
        return f"Record {self.serial_number} for {self.user.username} ({self.enum_status}, {self.ai_status})"
