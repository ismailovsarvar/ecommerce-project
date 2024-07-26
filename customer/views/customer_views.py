import csv
import json
from io import BytesIO

import openpyxl
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from customer.forms import CustomerModelForm
from customer.models import Customer

# Create your views here.

"""TEMPLATE VIEW"""


class CustomerTemplateView(TemplateView):
    template_name = 'customer/customer-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        search_query = self.request.GET.get('search')

        if search_query:
            customer_list = Customer.objects.filter()
            Q(full_name__icontains=search_query) | Q(address__icontains=search_query)

        else:
            customer_list = Customer.objects.all()

        paginator = Paginator(customer_list, 3)

        try:
            customer_page_obj = paginator.page(page)
        except PageNotAnInteger:
            customer_page_obj = paginator.page(1)
        except EmptyPage:
            customer_page_obj = paginator.page(paginator.num_pages)

        context['customer_page_obj'] = customer_page_obj
        context['customer_list'] = customer_list
        return context


class AddCustomerTemplateView(TemplateView):
    template_name = 'customer/add-customer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CustomerModelForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CustomerModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customers')
        return self.render_to_response(self.get_context_data(form=form))


class EditCustomerTemplateView(TemplateView):
    template_name = 'customer/add-customer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(id=self.kwargs['pk'])
        context['form'] = CustomerModelForm(instance=customer)
        return context

    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=self.kwargs['pk'])
        form = CustomerModelForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers')
        return self.render_to_response(self.get_context_data(form=form))


class DeleteCustomerTemplateView(TemplateView):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=self.kwargs['pk'])
        customer.delete()
        return redirect('customers')


class ExportDataTemplateView(TemplateView):

    def get(self, request, *args, **kwargs):
        format = request.GET.get('format', 'csv')
        if format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="customers.csv"'
            writer = csv.writer(response)
            writer.writerow(['ID', 'Full Name', 'Email', 'Phone Number', 'Address'])
            for customer in Customer.objects.all():
                writer.writerow(
                    [customer.id, customer.full_name, customer.email, customer.phone_number, customer.address])

        elif format == 'json':
            response = HttpResponse(content_type='application/json')
            data = list(Customer.objects.all().values('full_name', 'email', 'phone_number', 'address'))
            response.write(json.dumps(data, indent=4))
            response['Content-Disposition'] = 'attachment; filename=customers.json'

        elif format == 'xlsx':
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="customers.xlsx"'
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.append(['ID', 'Full Name', 'Email', 'Phone Number', 'Address'])

            for customer in Customer.objects.all():
                sheet.append([customer.id, customer.full_name, customer.email, customer.phone_number, customer.address])

            stream = BytesIO()
            workbook.save(stream)
            stream.seek(0)
            response.write(stream.read())

        else:
            response = HttpResponse(status=404)
            response.content = 'Bad request'

        return response


"""END TEMPLATE VIEW"""

"""Example Annotate"""
from django.db.models import Count, Avg
from django.views.generic import ListView


class CustomerListView(ListView):
    model = Customer
    template_name = 'customer/customer-list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        # Assume there is a related 'orders' field in Customer model
        return Customer.objects.annotate(order_count=Count('orders')).all()


"""Example Aggregate"""


def export_data(request):
    format = request.GET.get('format', 'csv')

    # Customerlarni umumiy sonini olish
    customer_stats = Customer.objects.aggregate(total_customers=Count('id'))

    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="customers.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Full Name', 'Email', 'Phone Number', 'Address'])
        for customer in Customer.objects.all():
            writer.writerow([customer.id, customer.full_name, customer.email, customer.phone_number, customer.address])

    elif format == 'json':
        response = HttpResponse(content_type='application/json')
        data = list(Customer.objects.all().values('full_name', 'email', 'phone_number', 'address'))
        response.write(json.dumps(data, indent=4))
        response['Content-Disposition'] = 'attachment; filename=customers.json'

    response['X-Total-Customers'] = customer_stats['total_customers']

    return response

# def customers(request):
#     page = request.GET.get('page', )
#     customer_list = Customer.objects.all()
#     paginator = Paginator(customer_list, 3)
#     try:
#         page_number = int(page)
#     except (ValueError, TypeError):
#         page_number = 1
#
#     try:
#         customer_page_obj = paginator.page(page_number)
#     except PageNotAnInteger:
#         customer_page_obj = paginator.page(1)
#     except EmptyPage:
#         customer_page_obj = paginator.page(paginator.num_pages)
#
#     search_query = request.GET.get('search')
#     if search_query:
#         customer_list = Customer.objects.filter(
#             Q(full_name__icontains=search_query) | Q(address__icontains=search_query))
#     # else:
#     #     customer_list = Customer.objects.all()
#     context = {
#         'customer_page_obj': customer_page_obj,
#         'customer_list': customer_list,
#     }
#     return render(request, 'customer/customer-list.html', context)


# def add_customer(request):
#     form = CustomerModelForm()
#     if request.method == 'POST':
#         form = CustomerModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('customers')
#
#     context = {
#         'form': form,
#     }
#
#     return render(request, 'customer/add-customer.html', context)


# def delete_customer(request, pk):
#     customer = Customer.objects.get(id=pk)
#     if customer:
#         customer.delete()
#         messages.add_message(
#             request,
#             messages.SUCCESS,
#             'Customer successfully deleted'
#         )
#         return redirect('customers')


# def edit_customer(request, pk):
#     customer = Customer.objects.get(id=pk)
#     form = CustomerModelForm(instance=customer)
#     if request.method == 'POST':
#         form = CustomerModelForm(instance=customer, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#
#             return redirect('customers')
#     context = {
#         'form': form,
#     }
#     return render(request, 'customer/update-customer.html', context)


# def export_data(request):
#     format = request.GET.get('format', 'csv')
#     if format == 'csv':
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="customers.csv"'
#         writer = csv.writer(response)
#         writer.writerow(['ID', 'Full Name', 'Email', 'Phone Number', 'Address'])
#         for customer in Customer.objects.all():
#         writer.writerow([customer.id, customer.full_name, customer.email, customer.phone_number, customer.address])
#
#     elif format == 'json':
#         response = HttpResponse(content_type='application/json')
#         data = list(Customer.objects.all().values('full_name', 'email', 'phone_number', 'address'))
#         response.write(json.dumps(data, indent=4))
#         response['Content-Disposition'] = 'attachment; filename=customers.json'
#
#     elif format == 'xlsx':
#         response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#         response['Content-Disposition'] = 'attachment; filename="customers.xlsx"'
#         workbook = openpyxl.Workbook()
#         sheet = workbook.active
#         sheet.append(['ID', 'Full Name', 'Email', 'Phone Number', 'Address'])
#
#         for customer in Customer.objects.all():
#             sheet.append([customer.id, customer.full_name, customer.email, customer.phone_number, customer.address])
#
#         stream = BytesIO()
#         workbook.save(stream)
#         stream.seek(0)
#         response.write(stream.read())
#
#     else:
#         response = HttpResponse(status=404)
#         response.content = 'Bad request'
#
#     return response
