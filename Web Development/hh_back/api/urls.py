from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('companies/', views.CompanyList.as_view(), name='companyList'),
    path('companies/<int:pk>/', views.CompanyDetail.as_view(), name='companyDetail'),
    path('companies/<int:pk>/vacancies', views.CompanyVacancyList.as_view(), name='companyVacancyList'),
    path('vacancies/', views.VacancyList.as_view(), name='vacancyList'),
    path('vacancies/<int:pk>/', views.VacancyDetail.as_view(), name='vacancyDetail'),
    path('vacancies/top_ten/', views.VacancyTopList.as_view(), name='vacancyTopList'),
]