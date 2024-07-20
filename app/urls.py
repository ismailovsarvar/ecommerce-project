from django.urls import path

from app.views import (
    ProductListView,
    ProductDetailTemplateView,
    AddProductTemplateView,
    EditProductTemplateView,
    DeleteProductView,
    EmailFormView
)

urlpatterns = [
    path('index/', ProductListView.as_view(), name='index'),
    path('product_detail/<int:product_id>', ProductDetailTemplateView.as_view(), name='product_detail'),
    path('add-product/', AddProductTemplateView.as_view(), name='add_product'),
    path('update-product/<int:pk>', EditProductTemplateView.as_view(), name='update_product'),
    path('delete-product/<int:pk>', DeleteProductView.as_view(), name='product_delete'),
    path('send-email/', EmailFormView.as_view(), name='send_email'),
]
