from datetime import date
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from my_finances.forms import IncomeForm, OutcomeForm, BalanceForm
from my_finances.helpers import calculate_repetitive_total
from my_finances.models import Income, Outcome, Balance


class IncomeListView(ListView):
    # Marek is the best
    # Yes he is!
    model = Income
    paginate_by = 100
    template_name = 'my_finances/balance_income_outcome_list.html'
    extra_context = {'list_what': 'Income'}
    # queryset = Income.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Income.objects.filter(user=user)
    # context_object_name = 'income_list'
    # allow_empty = True


class IncomeDetailView(DetailView):
    model = Income
    template_name = 'my_finances/balance_income_outcome_detail.html'
    extra_context = {'detail_what': 'Income'}

    # queryset = Income.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Income.objects.filter(user=user)
    # context_object_name = 'income'


class IncomeCreatView(CreateView):
    model = Income
    form_class = IncomeForm
    template_name = 'my_finances/balance_income_outcome_form.html'
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
    template_name = 'my_finances/balance_income_outcome_form.html'
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
    template_name = 'my_finances/balance_income_outcome_confirm_delete.html'
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
    template_name = 'my_finances/balance_income_outcome_list.html'
    extra_context = {'list_what': 'Outcome'}

    def get_queryset(self):
        user = self.request.user
        return Outcome.objects.filter(user=user)


class OutcomeDetailView(DetailView):
    model = Outcome
    template_name = 'my_finances/balance_income_outcome_detail.html'
    extra_context = {'detail_what': 'Outcome'}

    def get_queryset(self):
        user = self.request.user
        return Outcome.objects.filter(user=user)


class OutcomeCreatView(CreateView):
    model = Outcome
    form_class = OutcomeForm
    template_name = 'my_finances/balance_income_outcome_form.html'
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
    template_name = 'my_finances/balance_income_outcome_form.html'
    extra_context = {'header': 'Update Outcome'}

    def get_queryset(self):
        user = self.request.user
        return Outcome.objects.filter(user=user)

    def get_success_url(self):
        messages.success(self.request, 'Outcome updated successfully!')
        return reverse('my_finances:outcome_detail', kwargs={'pk': self.object.pk})


class OutcomeDeleteView(DeleteView):
    model = Outcome
    template_name = 'my_finances/balance_income_outcome_confirm_delete.html'
    extra_context = {'delete_what': 'Outcome'}

    def get_queryset(self):
        user = self.request.user
        return Outcome.objects.filter(user=user)

    def get_success_url(self):
        messages.success(self.request, 'Outcome deleted successfully!')
        return reverse_lazy('my_finances:outcome_list')


class BalanceListView(ListView):
    model = Balance
    paginate_by = 100
    template_name = 'my_finances/balance_income_outcome_list.html'
    extra_context = {'list_what': 'Balance'}

    def get_queryset(self):
        user = self.request.user
        return Balance.objects.filter(user=user)


class BalanceDetailView(DetailView):
    model = Balance
    template_name = 'my_finances/balance_income_outcome_detail.html'
    extra_context = {'detail_what': 'Balance'}

    def get_queryset(self):
        user = self.request.user
        return Balance.objects.filter(user=user)


class BalanceCreatView(CreateView):
    model = Balance
    form_class = BalanceForm
    template_name = 'my_finances/balance_income_outcome_form.html'
    extra_context = {'header': 'Add Balance'}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, 'Balance created successfully!')
        return reverse_lazy('my_finances:balance_list')


class BalanceUpdateView(UpdateView):
    model = Balance
    form_class = BalanceForm
    template_name = 'my_finances/balance_income_outcome_form.html'
    extra_context = {'header': 'Update Balance'}

    def get_queryset(self):
        user = self.request.user
        return Balance.objects.filter(user=user)

    def get_success_url(self):
        messages.success(self.request, 'Balance updated successfully!')
        return reverse('my_finances:balance_detail', kwargs={'pk': self.object.pk})


class BalanceDeleteView(DeleteView):
    model = Balance
    template_name = 'my_finances/balance_income_outcome_confirm_delete.html'
    extra_context = {'delete_what': 'Balance'}

    def get_queryset(self):
        user = self.request.user
        return Balance.objects.filter(user=user)

    def get_success_url(self):
        messages.success(self.request, 'Balance deleted successfully!')
        return reverse_lazy('my_finances:balance_list')


def current_finances(request):
    last_balance = Balance.objects.filter(user=request.user, type=1).order_by('-date').first()
    if not last_balance:
        messages.warning(request, 'No current balance has been recorded. '
                                  'Please add at least one current balance record.')
        return render(request, 'my_finances/current_finances.html')

    today = date.today()
    # initialise totals with sums of non repetitive incomes and outcomes
    total_income = Income.objects\
        .filter(user=request.user, date__gte=last_balance.date, date__lte=today, repetitive=False)\
        .aggregate(total=Sum('value'))['total']
    total_income = 0 if total_income is None else total_income
    total_outcome = Outcome.objects\
        .filter(user=request.user, date__gte=last_balance.date, date__lte=today,  repetitive=False)\
        .aggregate(total=Sum('value'))['total']
    total_outcome = 0 if total_outcome is None else total_outcome

    # updated totals with repetitive
    for income in Income.objects.filter(user=request.user, repetitive=True):
        total_income += calculate_repetitive_total(income, last_balance, today)
    for outcome in Outcome.objects.filter(user=request.user, repetitive=True):
        total_outcome += calculate_repetitive_total(outcome, last_balance, today)

    context = {
        'last_balance': last_balance,
        'estimated_balance': last_balance.value + total_income - total_outcome,
        'total_income': total_income,
        'total_outcome': total_outcome
    }
    return render(request, 'my_finances/current_finances.html', context=context)


def finance_history(request):
    return render(request, 'my_finances/finance_history.html')
