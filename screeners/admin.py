from django.contrib import admin
from .models import Stock, WhatsAppLead
from django.contrib.auth.models import User

admin.site.register(Stock)
admin.site.register(WhatsAppLead)

