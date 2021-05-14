from datetime import datetime
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from my_finances.forms import IncomeForm
from my_finances.models import Income


class IncomeListView(ListView):
    model = Income
    paginate_by = 100
    # template_name = 'my_finances/income_list.html'
    # queryset = Income.objects.all()
    # context_object_name = 'income_list'
    # extra_context = {'marunio1': 'Hello Marunio', 'marunio2': 'What up?!'}
    # allow_empty = True


class IncomeDetailView(DetailView):
    model = Income
    # template_name = 'my_finances/income_list.html'
    # queryset = Income.objects.all()
    # context_object_name = 'income'
    # extra_context = {'marunio1': 'Hello Marunio', 'marunio2': 'What up?!'}


class IncomeCreatView(CreateView):
    model = Income
    form_class = IncomeForm
    # template_name = 'my_finances/income_form.html'
    # template_name_suffix = '_create_form'
    # extra_context = {'dupa': 'blada', 'hello': 'world', 'additiona_stuff': Outcome.objects.all()}
    # success_url = reverse_lazy('my_finances:income_list')

    # def post(self, request, *args, **kwargs):
    #     form_date = request.POST['date']
    #     form_date = datetime.strptime(form_date, '%Y-%m-%d')
    #     if (form_date - datetime.today()).days < 0:
    #         messages.error(self.request, 'Income can not be backdated')
    #         return super().get(request, *args, **kwargs)
    #     return super().post(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, 'Income created successfully!')
        return reverse_lazy('my_finances:income_list')


class IncomeUpdateView(UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = 'my_finances/income_form.html'
    # template_name_suffix = '_update_form'
    # queryset = Income.objects.all()
    # context_object_name = 'income'
    # extra_context = {'dupa': 'blada'}

    def get_success_url(self):
        messages.success(self.request, 'Income updated successfully!')
        return reverse('my_finances:income_detail', kwargs={'pk': self.object.pk})


class IncomeDeleteView(DeleteView):
    model = Income
    # template_name = 'my_finances/income_confirm_delete.html'
    # template_name_suffix = '_delete_form'
    # queryset = Income.objects.all()
    # context_object_name = 'income'
    # extra_context = {'dupa': 'blada'}

    def get_success_url(self):
        messages.success(self.request, 'Income deleted successfully!')
        return reverse_lazy('my_finances:income_list')
