from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


"""
Each ticket should have the following fields:

Title
Time / Date filed
Description
Name of user who filed ticket
Status of ticket (New / In Progress / Done / Invalid) --> hint: https://docs.djangoproject.com/en/3.0/ref/models/fields/#choices (Links to an external site.)Links to an external site.
Name of user assigned to ticket
Name of user who completed the ticket
"""


class CustomUserModel(AbstractUser):
    display_name = models.CharField(max_length=80)

    def __str__(self):
        return self.username


class TicketModel(models.Model):
    NEW = 'NEW'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'
    INVALID = 'INVALID'
    TICKET_STATUS_CHOICES = [
        (NEW, 'New'),
        (IN_PROGRESS, 'In_Progress'),
        (DONE, 'Done'),
        (INVALID, 'invalid'),
    ]
    title = models.CharField(max_length=70)
    date_time = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=250)
    created_by = models.ForeignKey(CustomUserModel, null=True, on_delete=models.CASCADE, related_name='created_by')
    status = models.CharField(max_length=30, choices=TICKET_STATUS_CHOICES, default=NEW)
    assigned_to = models.ForeignKey(CustomUserModel, null=True,  on_delete=models.CASCADE, related_name='assigned_to')
    completed_by = models.ForeignKey(CustomUserModel, null=True,  on_delete=models.CASCADE, related_name='completed_by')

    def __str__(self):
        return self.title
