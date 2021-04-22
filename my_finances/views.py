from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from my_finances.models import Income


class IncomeListView(ListView):
    model = Income
    paginate_by = 100


class IncomeDetailView(DetailView):
    model = Income


class IncomeCreatView(CreateView):
    model = Income
    fields = ['value', 'date', 'type', 'repetitive', 'repetition_interval', 'repetition_time']
    success_url = reverse_lazy('my_finances:income_list')


class IncomeUpdateView(UpdateView):
    model = Income
    fields = ['value', 'date', 'type', 'repetitive', 'repetition_interval', 'repetition_time']
    success_url = reverse_lazy('my_finances:income_list')


class IncomeDeleteView(DeleteView):
    model = Income
    success_url = reverse_lazy('my_finances:income_list')
