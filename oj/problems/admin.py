from django.contrib import admin
from .models import Problem
from .models import Testcase

admin.site.register(Problem)
@admin.register(Testcase)
class TestcaseAdmin(admin.ModelAdmin):
    list_display = ('problem', 'order', 'is_sample')
    list_filter  = ('problem','is_sample')
    ordering     = ('problem','order')