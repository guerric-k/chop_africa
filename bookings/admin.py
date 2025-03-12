from django.contrib import admin
from .models import Table, Reservation



# Register your models here.
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'location')
    list_filter = ('capacity', 'location')
    search_fields = ('number', 'location')

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'table', 'number_of_guests', 'status')
    list_filter = ('date', 'status', 'has_children', 'is_disabled')
    search_fields = ('user__username', 'user__email', 'special_requests')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'table', 'date', 'time', 'number_of_guests', 'status')
        }),
        ('Special Accommodations', {
            'fields': ('has_children', 'number_of_children', 'is_disabled', 'disability_details')
        }),
        ('Additional Information', {
            'fields': ('special_requests', 'created_at', 'updated_at')
        }),
    )

admin.site.register(Table, TableAdmin)
admin.site.register(Reservation, ReservationAdmin)