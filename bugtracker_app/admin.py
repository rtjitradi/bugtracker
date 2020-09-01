from django.contrib import admin
from bugtracker_app.models import CustomUserModel, TicketModel


# Register your models here.
admin.site.register(CustomUserModel)
admin.site.register(TicketModel)
