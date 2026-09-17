from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import (
    Dealer, VehicleModel, Section, Station, Category, IssueType,
    Employee, Vehicle, RedTag
)


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'dealer']
    list_filter = ['dealer']
    search_fields = ['name', 'code']


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['code', 'description', 'show_in_form']
    list_filter = ['show_in_form']
    search_fields = ['code']


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ['name', 'section', 'show_in_form']
    list_filter = ['section', 'show_in_form']
    search_fields = ['name', 'section__code']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(IssueType)
class IssueTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_no', 'full_name', 'role', 'active']
    search_fields = ['employee_no', 'full_name']
    list_filter = ['active', 'role']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['chassis_no', 'model', 'dealer', 'lot', 'vi_size']
    search_fields = ['chassis_no']
    list_filter = ['model', 'dealer']


class RedTagResource(resources.ModelResource):
    vehicle = fields.Field(
        column_name='chassis_no',
        attribute='vehicle',
        widget=ForeignKeyWidget(Vehicle, 'chassis_no')
    )
    section = fields.Field(
        column_name='section',
        attribute='section',
        widget=ForeignKeyWidget(Section, 'code')
    )
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name')
    )
    raised_by = fields.Field(
        column_name='raised_by_employee_no',
        attribute='raised_by',
        widget=ForeignKeyWidget(Employee, 'employee_no')
    )

    class Meta:
        model = RedTag
        fields = (
            'id', 'date_raised', 'vehicle', 'section', 'station',
            'part_number', 'part_name', 'quantity', 'issue_description',
            'category', 'issue_type', 'raised_by', 'status',
            'closing_date', 'verified_by', 'remarks', 'location',
        )
        export_order = fields


@admin.register(RedTag)
class RedTagAdmin(ImportExportModelAdmin):
    resource_class = RedTagResource
    list_display = [
        'id', 'date_raised', 'vehicle', 'section', 'station',
        'category', 'issue_type', 'status', 'closing_date',
    ]
    list_filter = ['status', 'section', 'category', 'location', 'date_raised']
    search_fields = ['vehicle__chassis_no', 'issue_description', 'part_number']
    date_hierarchy = 'date_raised'
    autocomplete_fields = ['vehicle', 'raised_by', 'verified_by', 'station', 'issue_type']
