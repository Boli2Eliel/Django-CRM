import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from client.models import Client
from .forms import SignUpForm, AddRecordForm
from .models import Record


def login_user(request):
    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('dashboard')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('login')
    else:
        return render(request, 'home.html')

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('login')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('dashboard')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})

@login_required
def dashboard(request):
    thirty_days_ago = datetime.date.today() - datetime.timedelta(days=30)
    records = Record.objects.filter(converted_to_client=False, created_at__gte=thirty_days_ago).order_by(
        '-created_at')[0:4]
    clients = Client.objects.filter(created_at__gte=thirty_days_ago).order_by('-created_at')[0:4]


    # Leads and clients for Superuser
    total_record_count_all = Record.objects.all().count()
    total_clients_count_all = Client.objects.all().count()

    # Leads and clients for All
    total_record_count_user = Record.objects.filter(created_by=request.user).count()
    total_clients_count_user = Client.objects.filter(created_by=request.user).count()

    # By TEAM
    #total_lead_count = Lead.objects.filter(team=team).count()
    #total_client_count = Client.objects.filter(team=team).count()

    total_records_in_past30 = Record.objects.filter(created_at__gte=thirty_days_ago).count()

    # Converted to clients for superuser
    converted_to_clients = Record.objects.filter( converted_to_client=True).count()

    # Converted to clients for superuser
    converted_to_clients_user = Record.objects.filter(converted_to_client=True, created_by=request.user).count()

    context = {
        "records": records,
        "clients": clients,
        "total_record_count_all": total_record_count_all,
        "total_clients_count_all": total_clients_count_all,
        "total_record_count_user": total_record_count_user,
        "total_clients_count_user": total_clients_count_user,
        "converted_to_clients_user": converted_to_clients_user,
        "total_records_in_past30": total_records_in_past30,
        "converted_to_clients": converted_to_clients
    }

    return render(request, "website/dashboard.html", context)

@login_required
def list_record(request):
    records = Record.objects.filter(created_by=request.user, converted_to_client=False)
    return render(request, 'website/record_list.html', {'records': records})


@login_required
def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look Up Records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')


@login_required
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect('home')
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect('home')


class RecordCreateView(LoginRequiredMixin, CreateView):
    model = Record
    form_class = AddRecordForm
    success_url = reverse_lazy('record_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ajout prospect'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return redirect(self.get_success_url())


@login_required
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


class ConvertToClientView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        record = get_object_or_404(Record, created_by=request.user, pk=pk)
        client = Client.objects.create(
            firm=record.firm,
            first_name=record.first_name,
            last_name=record.last_name,
            email=record.email,
            phone=record.phone,
            address=record.address,
            created_by=request.user,
            zipcode=record.zipcode,
            city=record.city,
            country=record.country,
            converted_date=datetime.datetime.now()
        )
        record.converted_to_client = True
        record.save()
        messages.success(request, 'Le prospect a été converti en client avec succès!')

        return redirect('record_list')

# --------------- Show message and redirect ---------------


"""
ARCHIVES


@login_required
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')

"""