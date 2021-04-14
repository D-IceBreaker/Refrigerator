from django.shortcuts import render
from django.views import generic

from .models import Company, Vacancy

class IndexView(generic.TemplateView):
    template_name = 'api/index.html'

class CompanyList(generic.ListView):
    model = Company
    template_name = 'api/companyList.html'

class CompanyDetail(generic.DetailView):
    model = Company
    template_name = 'api/companyDetail.html'

class CompanyVacancyList(generic.DetailView):
    model = Company
    template_name = 'api/companyVacancyList.html'

class VacancyList(generic.ListView):
    model = Vacancy
    template_name = 'api/vacancyList.html'

class VacancyDetail(generic.DetailView):
    model = Vacancy
    template_name = 'api/vacancyDetail.html'

class VacancyTopList(generic.ListView):
    template_name = 'api/vacancyTopList.html'
    def get_queryset(self):
        return Vacancy.objects.order_by('-salary')[:10]
