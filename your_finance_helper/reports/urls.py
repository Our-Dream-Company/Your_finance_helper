from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReportsButtonsView.as_view(), name='reports'),
    path('detailed_current_financial_results', views.DetailedCurrentFinancialResultsView.as_view(
    ), name='detailed_current_financial_results')
]
