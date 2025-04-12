# screeners/urls.py

from django.urls import path
from .views import ScreenerDataView, TriggerScraperView, login_view, dashboard, create_whatsapp_lead
from django.views.generic import TemplateView


urlpatterns = [
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('api/screener/', ScreenerDataView.as_view(), name='get_screener_data'),
    path('api/scrape/', TriggerScraperView.as_view(), name='trigger_scraper'),
    path('api/whatsapp-leads/', create_whatsapp_lead, name='create_whatsapp_lead'),
    path('', TemplateView.as_view(template_name="landing2.html"), name="landing"),
]
