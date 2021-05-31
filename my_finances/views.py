from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from my_finances.forms import IncomeForm, OutcomeForm
from my_finances.models import Income, Outcome, Balance


class IncomeListView(ListView):
    model = Income
    paginate_by = 100
    template_name = 'my_finances/income_outcome_list.html'
    extra_context = {'list_what': 'Income'}
    # queryset = Income.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Income.objects.filter(user=user)
    # context_object_name = 'income_list'
    # allow_empty = True


class IncomeDetailView(DetailView):
    model = Income
    template_name = 'my_finances/income_outcome_detail.html'
    extra_context = {'detail_what': 'Income'}

    # queryset = Income.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Income.objects.filter(user=user)
    # context_object_name = 'income'


class IncomeCreatView(CreateView):
    model = Income
    form_class = IncomeForm
    template_name = 'my_finances/income_outcome_form.html'
    extra_context = {'header': 'Add Income'}

    # template_name_suffix = '_create_form'
    # success_url = reverse_lazy('my_finances:income_list')

    # def post(self, request, *args, **kwargs):
    #     form_date = request.POST['date']
    #     form_date = datetime.strptime(form_date, '%Y-%m-%d')
    #     if (form_date - datetime.today()).days < 0:
    #         messages.error(self.request, 'Income can not be backdated')
    #         return super().get(request, *args, **kwargs)
    #     return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, 'Income created successfully!')
        return reverse_lazy('my_finances:income_list')


class IncomeUpdateView(UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = 'my_finances/income_outcome_form.html'
    extra_context = {'header': 'Update Income'}
    # template_name_suffix = '_update_form'
    # queryset = Income.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Income.objects.filter(user=user)
    # context_object_name = 'income'

    def get_success_url(self):
        messages.success(self.request, 'Income updated successfully!')
        return reverse('my_finances:income_detail', kwargs={'pk': self.object.pk})


class IncomeDeleteView(DeleteView):
    model = Income
    template_name = 'my_finances/income_outcome_confirm_delete.html'
    extra_context = {'delete_what': 'Income'}
    # template_name_suffix = '_delete_form'
    # queryset = Income.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Income.objects.filter(user=user)
    # context_object_name = 'income'

    def get_success_url(self):
        messages.success(self.request, 'Income deleted successfully!')
        return reverse_lazy('my_finances:income_list')


class OutcomeListView(ListView):
    model = Outcome
    paginate_by = 100
    template_name = 'my_finances/income_outcome_list.html'
    extra_context = {'list_what': 'Outcome'}

    def get_queryset(self):
        user = self.request.user
        return Outcome.objects.filter(user=user)


class OutcomeDetailView(DetailView):
    model = Outcome
    template_name = 'my_finances/income_outcome_detail.html'
    extra_context = {'detail_what': 'Outcome'}

    def get_queryset(self):
        user = self.request.user
        return Outcome.objects.filter(user=user)


class OutcomeCreatView(CreateView):
    model = Outcome
    form_class = OutcomeForm
    template_name = 'my_finances/income_outcome_form.html'
    extra_context = {'header': 'Add Outcome'}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, 'Outcome created successfully!')
        return reverse_lazy('my_finances:outcome_list')


class OutcomeUpdateView(UpdateView):
    model = Outcome
    form_class = OutcomeForm
    template_name = 'my_finances/income_outcome_form.html'
    extra_context = {'header': 'Update Outcome'}

    def get_queryset(self):
        user = self.request.user
        return Outcome.objects.filter(user=user)

    def get_success_url(self):
        messages.success(self.request, 'Outcome updated successfully!')
        return reverse('my_finances:outcome_detail', kwargs={'pk': self.object.pk})


class OutcomeDeleteView(DeleteView):
    model = Outcome
    template_name = 'my_finances/income_outcome_confirm_delete.html'
    extra_context = {'delete_what': 'Outcome'}

    def get_queryset(self):
        user = self.request.user
        return Outcome.objects.filter(user=user)

    def get_success_url(self):
        messages.success(self.request, 'Outcome deleted successfully!')
        return reverse_lazy('my_finances:outcome_list')
