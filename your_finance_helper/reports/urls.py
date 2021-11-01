from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReportsButtonsView.as_view(), name='reports'),
    path('detailed_current_financial_results', views.DetailedCurrentFinancialResultsView.as_view(
    ), name='detailed_current_financial_results'),
    path('detailed_current_financial_results/<int:pk>',
         views.TransactionView.as_view(), name='transaction_view'),
    path('detailed_current_financial_results/<int:pk>/update',
         views.TransactionUpdateView.as_view(), name='transaction_update'),
    path('detailed_current_financial_results/<int:pk>/delete',
         views.TransactionDeleteView.as_view(), name='transaction_delete'),
    path('detailed_current_financial_results/report_for_the_period/',
         views.ReportForThePeriod.as_view(), name='report_for_the_period')
]
