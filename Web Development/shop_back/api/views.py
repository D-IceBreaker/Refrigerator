from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Product, Category

class IndexView(generic.TemplateView):
    template_name = 'api/index.html'

class ProductList(generic.ListView):
    model = Product
    template_name = 'api/product_list.html'

class ProductDetail(generic.DetailView):
    model = Product
    template_name = 'api/product_detail.html'

class CategoriesList(generic.ListView):
    model = Category
    template_name = 'api/category_list.html'

class CategoryDetail(generic.DetailView):
    model = Category
    template_name = 'api/category_detail.html'