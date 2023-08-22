import datetime

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


def home(request):
	records = Record.objects.filter(created_by=request.user, converted_to_client=False)
	# Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('home')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('home')
	else:
		return render(request, 'home.html', {'records':records})



def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')


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
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})



def customer_record(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		customer_record = Record.objects.get(id=pk)
		return render(request, 'record.html', {'customer_record':customer_record})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')



def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = Record.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted Successfully...")
		return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')

class RecordCreateView(LoginRequiredMixin,CreateView):
	model = Record
	form_class = AddRecordForm
	success_url = reverse_lazy('home')
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Ajout prospect'
		return context
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.created_by = self.request.user
		self.object.save()
		return redirect(self.get_success_url())

def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():

				add_record = form.save()
				messages.success(request, "Record Added...")
				return redirect('home')
		return render(request, 'add_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')


def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')

class ConvertToClientView(LoginRequiredMixin,View):
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

		return redirect('home')


# --------------- Show message and redirect ---------------



