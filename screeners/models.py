from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

def default_end_date():
    return timezone.now() + timedelta(days=3)

class Stock(models.Model):
    SCREENER_CHOICES = (
        ('intraday', 'Intraday Screener'),
        ('short_term', 'Short Term'),
        ('long_term', 'Long Term'),
        ('multibagger', 'Multi Bagger'),
        ('intraday_multibagger', 'Intraday Multi Bagger'),
    )
    screener_type = models.CharField(max_length=50, choices=SCREENER_CHOICES)
    stock_symbol = models.CharField(max_length=20)
    stock_name = models.CharField(max_length=100)
    cmp_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # New field for CMP price

    # Add additional fields as needed
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.stock_symbol} - {self.stock_name}"


class WhatsAppLead(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=10, unique=True, help_text="10-digit Indian WhatsApp number")
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    end_date = models.DateTimeField(default=default_end_date, null=True)

    def __str__(self):
        return f"{self.number} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"