from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='main_page'),
    path('add_income', views.AddIncomeView.as_view(), name='add_income'),
    path('add_outcome', views.AddOutcomeView.as_view(), name='add_outcome'),
    path('add_new_section', views.AddNewSectionView.as_view(),
         name='add_new_section'),
    path('add_new_category', views.AddNewCategoryView.as_view(),
         name='add_new_category'),
    path('add_new_name_operation', views.AddNewNameOperationView.as_view(),
         name='add_new_name_operation'),
]
