from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('categories/', views.CategoriesList.as_view(), name='categories_list'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category_detail'),
]