
from catalog.apps import CatalogConfig
from django.contrib.auth.views import LoginView
from django.views.decorators.cache import cache_page
from django.urls import path
from catalog.views import contacts,ProductListView, CategoryListView, ProductDetailView, \
    ProductCreateView, ProductUpdateView, RecordCreateView
# ProductListView, RecordListView,  ProductDeleteView, RecordDetailView,
app_name = CatalogConfig.name

urlpatterns = [
    path('', cache_page(60)(ProductListView.as_view()), name='home'),
    path('categories/', cache_page(60)(CategoryListView.as_view()), name='categories'),
    path('contacts/', cache_page(60)(contacts), name='contacts'),
    path('cards/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    # path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    # path('records/', RecordListView.as_view(), name='records_list'),
    # path('records/<slug:slug>/', RecordDetailView.as_view(), name='record_detail'),
    path('record/create/', RecordCreateView.as_view(), name='record_create'),
]
