from django.db import models

class OrderPrediction(models.Model):
    # Transaction & Product Inputs
    price = models.DecimalField(max_digits=8, decimal_places=2)
    manufacturer_id = models.IntegerField()
    delivery_duration = models.IntegerField(help_text="Estimated delivery transit in days")
    is_delivery_missing = models.BooleanField(default=False)
    
    # Customer Demographics & Behavior
    customer_age = models.FloatField()
    account_age_days = models.IntegerField()
    order_month = models.IntegerField()
    salutation = models.CharField(max_length=20)
    state = models.CharField(max_length=60)
    order_day_of_week = models.CharField(max_length=20)
    
    # E-Commerce Behavioral Indicators
    is_bracketed = models.BooleanField(default=False, help_text="Ordered multiple sizes of same item")
    is_unsized = models.BooleanField(default=False, help_text="Unsized accessory item")
    
    # Model Output Metrics
    prediction_label = models.CharField(max_length=30)  # e.g., 'High Return Risk' or 'Likely to Keep'
    return_probability = models.FloatField()             # e.g., 68.4
    is_high_risk = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} | {self.prediction_label} ({self.return_probability}%)"