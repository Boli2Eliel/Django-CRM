from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from client.forms import AddClientForm
from client.models import Client


def clients_list(request):
    clients = Client.objects.filter(created_by=request.user)
    return render(request, 'client/clients_list.html', {'clients': clients})


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "client/clients_list.html"

    def get_queryset(self):
        queryset = super(ClientListView, self).get_queryset()
        # converted_to_client = False : Pour faire de sorte qu'une fois converti en client le prospect doit disparaitre de cette liste
        return queryset.filter(created_by=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "client/client_detail.html"

    # get_context to add an extra data to class based views
    """def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['fileform'] = AddFileForm()
        return context"""

    def get_queryset(self):
        queryset = super(ClientDetailView, self).get_queryset()

        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    template_name = "client/client_form.html"
    form_class = AddClientForm
    success_url = reverse_lazy('clients:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ajout client'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return redirect(self.get_success_url())
