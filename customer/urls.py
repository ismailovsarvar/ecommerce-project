from django.urls import path

from customer.views.auth import (
    LoginPageView,
    logout_page,
    register_page,
    verify_email_done,
    verify_email_confirm
)
from customer.views.customer_views import (
    CustomerTemplateView,
    AddCustomerTemplateView,
    DeleteCustomerTemplateView,
    EditCustomerTemplateView,
    ExportDataTemplateView,
)

urlpatterns = [
    path('customer-list/', CustomerTemplateView.as_view(), name='customers'),
    path('add-customer/', AddCustomerTemplateView.as_view(), name='add_customer'),
    path('customer/<int:pk>/delete', DeleteCustomerTemplateView.as_view(), name='delete'),
    path('customer/<int:pk>/update', EditCustomerTemplateView.as_view(), name='edit'),
    # Authentication path
    path('login-page/', LoginPageView.as_view(), name='login'),
    path('logout-page/', logout_page, name='logout'),
    path('register-page/', register_page, name='register'),
    path('export-data/', ExportDataTemplateView.as_view(), name='export_data'),
    # sending
    path('verify-email-done/', verify_email_done, name='verify_email_done'),
    path('verify-email-confirm/<uidb64>/<token>/', verify_email_confirm, name='verify_email_confirm'),
]
