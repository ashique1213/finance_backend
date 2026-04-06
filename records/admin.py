from django.contrib import admin
from .models import Category, FinancialRecord

admin.site.register(Category)
admin.site.register(FinancialRecord)