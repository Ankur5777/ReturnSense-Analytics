from django.contrib import admin
from .models import OrderPrediction

@admin.register(OrderPrediction)
class OrderPredictionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'price', 
        'delivery_duration', 
        'customer_age', 
        'is_bracketed', 
        'prediction_label', 
        'return_probability', 
        'created_at'
    )
    list_filter = ('is_high_risk', 'is_bracketed', 'is_unsized', 'state', 'created_at')
    search_fields = ('id', 'state', 'salutation')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)