from django.contrib import admin

# Register your models here.

from .models import Data_base_Transaction


class TxAdmin(admin.ModelAdmin):
    list_display = ('Txid', 'description')

# Register the admin class with the associated model
admin.site.register(Data_base_Transaction, TxAdmin)