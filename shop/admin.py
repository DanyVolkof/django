from django.contrib import admin
from .models import Shop, Organization


# Register your models here.



class ShopInline(admin.TabularInline):
    model = Shop

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [ShopInline]

admin.site.register(Organization, OrganizationAdmin)


