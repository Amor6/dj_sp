
from catalog.apps import CatalogConfig
from django.contrib.auth.views import LoginView
from django.views.decorators.cache import cache_page
from django.urls import path
from catalog.views import ProductListView, CategoryListView, ProductDetailView, \
    ProductCreateView, ProductUpdateView, RecordCreateView, ContactView
# ProductListView, RecordListView,  ProductDeleteView, RecordDetailView,
app_name = CatalogConfig.name

urlpatterns = [
    path('',ProductListView.as_view(), name='home'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('contacts/', ContactView.as_view(template_name='catalog/contacts.html'), name='contacts'),
    path('cards/<int:pk>/', cache_page(60)(ProductDetailView.as_view(template_name='catalog/product_detail.html')), name='product'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    # path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    # path('records/', RecordListView.as_view(), name='records_list'),
    # path('records/<slug:slug>/', RecordDetailView.as_view(), name='record_detail'),
    path('record/create/', RecordCreateView.as_view(), name='record_create'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
]
