"""bugtracker_config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bugtracker_app.views import index_view, login_view, userdetails_view, addnewticket_view, ticketdetails_view, editticket_view, assignticket_view, ticketdone_view, invalidticket_view, logout_view

urlpatterns = [
    path('', index_view, name='homepage'),
    path('login/', login_view, name='login'),
    path('userdetails/', userdetails_view, name='userdetails'),
    path('addnewticket/', addnewticket_view, name='addnewticket'),
    path('ticket/<int:ticker_id>/', ticketdetails_view, name='ticketdetails'),
    path('ticket/<int:ticket_id>/edit/', editticket_view, name='editticket'),
    path('ticket/<int:ticket_id>/', assignticket_view, name='assignticket'),
    path('ticket/<int:ticket_id>/', ticketdone_view, name='ticketdone'),
    path('ticket/<int:ticket_id>', invalidticket_view, name='invalidticket'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),
]
