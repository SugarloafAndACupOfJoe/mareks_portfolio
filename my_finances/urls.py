from django.urls import path

from my_finances import views


app_name = 'my_finances'


urlpatterns = [
    path('income_list/', views.IncomeListView.as_view(), name='income_list'),
    path('income_detail/<pk>', views.IncomeDetailView.as_view(), name='income_detail'),
    path('income_create/', views.IncomeCreatView.as_view(), name='income_create'),
    path('income_update/<pk>', views.IncomeUpdateView.as_view(), name='income_update'),
    path('income_delete/<pk>', views.IncomeDeleteView.as_view(), name='income_delete'),

    path('outcome_list/', views.OutcomeListView.as_view(), name='outcome_list'),
    path('outcome_detail/<pk>', views.OutcomeDetailView.as_view(), name='outcome_detail'),
    path('outcome_create/', views.OutcomeCreatView.as_view(), name='outcome_create'),
    path('outcome_update/<pk>', views.OutcomeUpdateView.as_view(), name='outcome_update'),
    path('outcome_delete/<pk>', views.OutcomeDeleteView.as_view(), name='outcome_delete'),

    path('balance_list/', views.BalanceListView.as_view(), name='balance_list'),
    path('balance_detail/<pk>', views.BalanceDetailView.as_view(), name='balance_detail'),
    path('balance_create/', views.BalanceCreatView.as_view(), name='balance_create'),
    path('balance_update/<pk>', views.BalanceUpdateView.as_view(), name='balance_update'),
    path('balance_delete/<pk>', views.BalanceDeleteView.as_view(), name='balance_delete'),

    path('current_period/', views.current_period, name='current_period'),
    path('year_overview/', views.year_overview, name='year_overview'),

    path('get_summary_tiles/', views.get_summary_tiles,
         name='get_summary_tiles'),
    path('get_year_chart/', views.get_year_chart,
         name='get_year_chart'),
    path('get_income_or_outcome_by_type/', views.get_income_or_outcome_by_type,
         name='get_income_or_outcome_by_type'),
]
