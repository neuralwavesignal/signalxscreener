from django.db import models

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
    number = models.CharField(max_length=10, unique=True, help_text="10-digit Indian WhatsApp number")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number