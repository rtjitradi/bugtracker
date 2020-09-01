from django.shortcuts import render, HttpResponseRedirect, reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout

from bugtracker_app.models import TicketModel
from bugtracker_app.forms import LoginForm, NewTicketForm

from bugtracker_config.settings import AUTH_USER_MODEL


"""
When a ticket is filed/created, it should have the following settings:

Status: New
User Assigned: None
User who Completed: None
User who filed: Person who's logged in
When a ticket is assigned, these change as follows:

Status: In Progress
User Assigned: person the ticket now belongs to
User who Completed: None
When a ticket is Done, these change as follows:

Status: Done
User Assigned: None
User who Completed: person who the ticket used to belong to
When a ticket is marked as Invalid, these change as follows:

Status: Invalid
User Assigned: None
User who Completed: None

superuser
username: reggy
password: djangoway
"""


@login_required
def index_view(request):
    all_tickets = TicketModel.objects.all()
    return render(request, 'index.html', {'page_title': 'BugTracker: Homepage', 'all_tickets': all_tickets})


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_data = login_form.cleaned_data
            authenticated_user = authenticate(request, username=login_data.get('username'), password=login_data.get('password'))
            if authenticated_user:
                login(request, authenticated_user)
                return HttpResponseRedirect(request.GET.get('next', reverse('homepage')))

    login_form = LoginForm()
    return render(request, 'login.html', {'page_title': 'BugTracker: Login Form', 'login_form': login_form})


@login_required
# https://stackoverflow.com/questions/30681061/django-queryset-by-username-in-user-model
def userdetails_view(request, user_name):
    authorized_user = TicketModel.objects.filter(created_by__username=user_name).first()
    user_tickets = TicketModel.objects.filter(created_by__username=user_name)
    return render(request, 'userdetails.html', {'page_title': 'BugTracker: User Details', 'login_user': authorized_user, 'user_tickets': user_tickets})


@login_required
def addnewticket_view(request):
    if request.method == 'POST':
        newticket_form = NewTicketForm(request.POST)
        if newticket_form.is_valid():
            newticket_data = newticket_form.cleaned_data
            TicketModel.objects.create(
                title=newticket_data.get('title'),
                description=newticket_data.get('description'),
                created_by=request.user
            )
            return HttpResponseRedirect(reverse('homepage'))

    newticket_form = newticket_form()
    return render(request, 'addnewticket.html', {'page_title': 'BugTracker: Add New Ticket', 'newticket_form': newticket_form})


@login_required
def ticketdetails_view(request, ticket_id):
    ticket = TicketModel.objects.get(id=ticket_id).first()
    return render(request, 'ticketdetails.html', {'page_title': 'BugTracker: Ticket Details', 'ticket': ticket})


@login_required
def editticket_view(request, ticket_id):
    edit_ticket = TicketModel.objects.get(id=ticket_id)
    if request.method == 'POST':
        edit_form = NewTicketForm(request.POST)
        if edit_form.is_valid():
            edit_data = edit_form.cleaned_data
            edit_ticket.title = edit_data['title']
            edit_ticket.description = edit_data['description']
            edit_ticket.save()
            return HttpResponseRedirect(reverse('ticketdetails', args=[edit_ticket.id]))

    edit_data = {'title': edit_ticket.title, 'description': edit_ticket.description}
    edit_form = NewTicketForm(initial=edit_data)
    return render(request, 'editticket.html', {'page_title': 'BugTracker: Edit Ticket', 'edit_form': edit_form})


@login_required
def assignticket_view(request, ticket_id):
    assign_ticket = TicketModel.objects.get(id=ticket_id)
    assign_ticket.status = 'In Progress'
    assign_ticket.assigned_to = request.user
    assign_ticket.completed_by = None
    assign_ticket.save()
    return HttpResponseRedirect(reverse('ticketdetails', args=[assign_ticket.id]))


@login_required
def ticketdone_view(request, ticket_id):
    ticket_done = TicketModel.object.get(id=ticket_id)
    ticket_done.status = 'Done'
    ticket_done.assigned_to = None
    ticket_done.completed_by = request.user
    ticket_done.save()
    return HttpResponseRedirect(reverse('ticketdetails', args=[ticket_done.id]))


@login_required
def invalidticket_view(request, ticket_id):
    invalid_ticket = TicketModel.object.get(id=ticket_id)
    invalid_ticket.status = 'Invalid'
    invalid_ticket.assigned_to = None
    invalid_ticket.completed_by = None
    invalid_ticket.save()
    return HttpResponseRedirect(reverse('ticketdetails', args=[invalid_ticket.id]))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))
