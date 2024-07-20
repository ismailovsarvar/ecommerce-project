from django.contrib import admin

from customer.forms import UserModelForm
from customer.models import Customer, User
from adminsortable2.admin import SortableAdminMixin


# Register your models here.
# admin.site.register(Customer)

@admin.register(Customer)
class CustomerModelAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'is_active']
    search_fields = ['email', 'id']
    list_filter = ['joined', 'is_active']
    ordering = ('-joined', 'order')

    def has_add_permission(self, request):
        return True

    def has_view_or_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(User)
class UserModelAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['email', 'username', 'birth_of_date', 'is_superuser']
    form = UserModelForm
    ordering = ('order',)
