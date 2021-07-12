from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='main_page'),
    path('add_income', views.AddIncomeView.as_view(), name='add_income'),
    path('add_outcome', views.AddOutcomeView.as_view(), name='add_outcome')
]
