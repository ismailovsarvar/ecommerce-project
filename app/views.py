from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from app.forms import ProductModelForm, EmailForm
from app.models import Product

# Create your views here.

"""The beginning of receiving products"""

""" Method - 1 """

# def index(request):
#     page = request.GET.get('page', '')
#     products = Product.objects.all().order_by('-id')
#     paginator = Paginator(products, 2)
#     try:
#         page_obj = paginator.page(page)
#     except PageNotAnInteger:
#         page_obj = paginator.page(1)
#     except EmptyPage:
#         page_obj = paginator.page(paginator.num_pages)
#
#     context = {
#         'products': products,
#         'page_obj': page_obj,
#
#     }
#     return render(request, 'product/index.html', context)


""" Method - 2 """

# class ProductListView(View):
#
#     def get(self, request):
#         page = request.GET.get('page', '')
#         products = Product.objects.all().order_by('-id')
#         paginator = Paginator(products, 2)
#         try:
#             page_obj = paginator.page(page)
#         except PageNotAnInteger:
#             page_obj = paginator.page(1)
#         except EmptyPage:
#             page_obj = paginator.page(paginator.num_pages)
#
#         context = {
#             'products': products,
#             'page_obj': page_obj,
#
#         }
#         return render(request, 'product/index.html', context)


"""Example Aggregate"""
from django.db.models import Avg

# class ProductListView(View):
#     def get(self, request):
#         page = request.GET.get('page', '')
#         products = Product.objects.all().order_by('-id')
#         paginator = Paginator(products, 2)
#
#         # Aggregate: Get the total number of products and average price
#         product_stats = Product.objects.aggregate(total_products=Count('id'), average_price=Avg('price'))
#
#         try:
#             page_obj = paginator.page(page)
#         except PageNotAnInteger:
#             page_obj = paginator.page(1)
#         except EmptyPage:
#             page_obj = paginator.page(paginator.num_pages)
#
#         context = {
#             'products': products,
#             'page_obj': page_obj,
#             'total_products': product_stats['total_products'],
#             'average_price': product_stats['average_price'],
#         }
#         return render(request, 'product/index.html', context)


"""Example Annotate"""


class ProductListView(View):
    def get(self, request):
        page = request.GET.get('page', '')
        products = Product.objects.all().order_by('-id').annotate(average_rating=Avg('reviews__rating'))
        paginator = Paginator(products, 2)

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            'products': products,
            'page_obj': page_obj,
        }
        return render(request, 'product/index.html', context)


"""End of receipt of products"""

"""The beginning of the product detail"""

""" Method - 1 """

# def product_detail(request, product_id):
#     product = Product.objects.get(id=product_id)
#     attributes = product.get_attributes()
#     contex = {
#         'product': product,
#         'attributes': attributes
#     }
#     return render(request, 'product/product-detail.html', contex)

""" Method - 2 """

# class ProductDetailView(View):
#     def get(self, request, product_id):
#         product = Product.objects.get(id=product_id)
#         attributes = product.get_attributes()
#
#         contex = {
#             'product': product,
#             'attributes': attributes
#         }
#         return render(request, 'product/product-detail.html', contex)


"""End of the product detail"""

"""Start of product addition"""

""" Method - 1 """
# def add_product(request):
#     form = ProductForm()
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         name = request.POST['name']
#         description = request.POST['description']
#         price = request.POST['price']
#         rating = request.POST['rating']
#         discount = request.POST['discount']
#         quantity = request.POST['quantity']
#         product = Product(name=name, description=description, price=price, rating=rating, discount=discount,
#                           quantity=quantity)
#         if form.is_valid():
#             product.save()
#             return redirect('index')
#
#     context = {
#         'form': form
#     }
#     return render(request, 'app/add-product.html', context)

# def add_product(request):
#     form = ProductModelForm()
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'product/add-product.html', context)

""" Method - 2 """

# class AddProductView(View):
#     def get(self, request):
#         form = ProductModelForm()
#         return render(request, 'product/add-product.html', {'form': form})
#
#     def post(self, request):
#         form = ProductModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')


"""End of product addition"""

"""Start of product editing"""
""" Method - 2 """

# class EditProductView(View):
#     def get(self, request, pk):
#         product = get_object_or_404(Product, id=pk)
#         form = ProductModelForm(instance=product)
#         return render(request, 'product/update-product.html', {'form': form})
#
#     def post(self, request, pk):
#         product = get_object_or_404(Product, id=pk)
#
#         form = ProductModelForm(instance=product, data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('product_detail', pk)


"""End of product editing"""

"""Start of product delete"""


class DeleteProductView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        if product:
            product.delete()
            return redirect('index')


"""End of product delete"""

"""TEMPLATE VIEW"""


class ProductDetailTemplateView(TemplateView):
    template_name = 'product/product-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(id=kwargs['product_id'])
        context['product'] = product
        context['attributes'] = product.get_attributes()
        return context


class EditProductTemplateView(TemplateView):
    template_name = 'product/update-product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(id=kwargs['pk'])
        context['form'] = ProductModelForm(instance=product)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        product = get_object_or_404(Product, id=kwargs['pk'])
        form = ProductModelForm(instance=product, data=request.POST)
        context['form'] = form
        if form.is_valid():
            form.save()
            return redirect('index')


class AddProductTemplateView(TemplateView):
    template_name = 'product/add-product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductModelForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        return self.render_to_response(self.get_context_data(form=form))


# SENDING EMAIL TEMPLATE VIEW


class EmailFormView(TemplateView):
    template_name = 'product/send_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EmailForm()
        return context

    def post(self, request, *args, **kwargs):
        form = EmailForm(request.POST)
        if form.is_valid():
            from_email = form.cleaned_data['from_email']
            to_email = form.cleaned_data['to_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(
                subject,
                message,
                from_email,
                [to_email],
                fail_silently=False,
            )
            return HttpResponse('Email sent successfully')
        return self.render_to_response(self.get_context_data(form=form))
