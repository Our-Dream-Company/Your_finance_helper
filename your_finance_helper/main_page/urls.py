from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main_page'),
    path('add_income', views.add_income, name='add_income'),
    path('add_outcome', views.add_outcome, name='add_outcome')
]
