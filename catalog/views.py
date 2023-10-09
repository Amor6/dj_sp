from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.forms import inlineformset_factory
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView
from catalog.models import Product, Version, Category, Record
from catalog.services import get_cached_versons_for_product, get_category_list


class CategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'catalog.view_category'
    model = Category
    template_name = 'catalog/categories.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['versions'] = get_cached_versons_for_product(self.object.pk)
        # context_data['object_list'] = get_category_list()
        return context_data


class ProductCreateView(CreateView):
    template_name = 'home.html'

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['formset'] = get_cached_versons_for_product(self.object.pk)
        SubjectFormset = inlineformset_factory(Product, Version, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = SubjectFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = SubjectFormset(instance=self.object)

        return context_data


class ProductUpdateView(UpdateView):
    model = Product
    permission_required = 'catalog.change_product'
    success_url = reverse_lazy('product_update.html')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Product, Version, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = SubjectFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = SubjectFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

class ProductListView(ListView):
    template_name = 'catalog/home.html'
    model = Product
    extra_context = {
        'object_list': Product.objects.all(),
        'title': 'Все продукты'  # дополнение к статической информации
    }


# class ProductDeleteView(DeleteView):
#     permission_required = 'catalog.delete_product'
#     model = Product
#     success_url = reverse_lazy('record_detail.html')


# class ProductListView(ListView):
#     permission_required = 'catalog.view_product'
#     model = Product
#     template_name = 'record_detail.html'
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super().get_context_data(*args, **kwargs)
#         version_list = Version.objects.all()
#         context_data['formset'] = version_list
#         return context_data


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        if self.object.author == self.request.user:
            context['edit_url'] = reverse('product_update', kwargs={'pk': self.object.pk})
        return context

# class RecordListView(ListView):  # выведение контекста записей из модели по ключу object_list
#     model = Record
#     template_name = 'record_detail.html'
#     context_object_name = 'records'
#     extra_context = {
#         'title': 'Все записи',  # дополнение к статической информации
#     }
#
#     def get_queryset(self):  # выводит только активные записи
#         queryset = super().get_queryset()
#         queryset = queryset.filter(sign_of_publication=True)
#         return queryset


# class RecordDetailView(DetailView):
#     model = Record
#     template_name = 'product_detail.html'
#     context_object_name = 'object'
#
#     def get_context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         context_data['title'] = self.get_object()
#         return context_data
#
#     def get_success_url(self):
#         return reverse_lazy('record_detail', kwargs={'slug': self.object.slug})


class RecordCreateView(CreateView):
    model = Record
    fields = ('record_title', 'slug', 'content', 'preview')
    success_url = reversed('records_list')



class ContactView(TemplateView):
    template_name = 'contacts.html'
    extra_context = {
        'title': 'Контакты'
    }