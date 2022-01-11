from django.contrib import admin
from .models import article
# Register your models here.

# admin.site.register(article)

@admin.register(article)
class articleAdmin(admin.ModelAdmin):
    list_display = ['idd','title','author','email','date']
