from django.contrib import admin
from .models import Table, Customer, TableDate

# Register your models here.


# Table MODEL
@admin.action(description="Mark selected tables as Available")
def table_available_action(modeladmin, request, queryset):
    queryset.update(status=Table.TableStatus.AVAILABLE)

class TableAdmin(admin.ModelAdmin):
    list_display = ['id', 'seats','status']
    actions = [table_available_action]

admin.site.register(Table, TableAdmin)


# TableDate MODEL
class TableDateAdmin(admin.ModelAdmin):
    list_display = ['name', 'table', 'date']
admin.site.register(TableDate, TableDateAdmin)


# Customer MODEL
@admin.action(description="Cancel selected reservations")
def cancel_reservation(modeladmin, request, queryset):
    queryset.update(table=None, time=None, date=None)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'table', 'date', 'time']
    actions = [cancel_reservation]

admin.site.register(Customer, CustomerAdmin)
