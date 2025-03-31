# screeners/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Stock
from .scraper import run_scraper_function
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
import json
from django.views.decorators.http import require_http_methods
from .models import WhatsAppLead
import random, string
from django.contrib.auth.models import User
from django.db import transaction



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required
def dashboard(request):
    # Retrieve all stock data (you can further group by screener_type in the template)
    from .models import Stock
    stocks = Stock.objects.all()
    return render(request, 'dashboard.html', {'stocks': stocks})


class ScreenerDataView(View):
    def get(self, request, *args, **kwargs):
        screener_type = request.GET.get('type')
        if screener_type:
            stocks = Stock.objects.filter(screener_type=screener_type)
        else:
            stocks = Stock.objects.all()
        data = [
            {
                'stock_symbol': s.stock_symbol,
                'stock_name': s.stock_name,
                'screener_type': s.screener_type,
                'last_updated': s.last_updated,
                'cmp_price':s.cmp_price
            }
            for s in stocks
        ]
        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class TriggerScraperView(View):
    def post(self, request, *args, **kwargs):
        run_scraper_function()
        return JsonResponse({'status': 'Scraping initiated'})
    

def generate_random_credentials():
    user_id = 'demo' + ''.join(random.choices(string.digits, k=4))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    email = user_id + '@gmail.com'
    return user_id , password, email


@csrf_exempt
@require_http_methods(["POST"])
def create_whatsapp_lead(request):
    with transaction.atomic():
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        number = data.get("number")
        if not number:
            return JsonResponse({"error": "Number field is required"}, status=400)
        if not number.isdigit() or len(number) != 10:
            return JsonResponse({"error": "Invalid number. Must be a 10-digit Indian WhatsApp number."}, status=400)
        
        if WhatsAppLead.objects.filter(number=number).exists():
            return JsonResponse({"error": "This number already exists."}, status=400)
        
        try:
            lead = WhatsAppLead.objects.create(number=number)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
        # Generate the demo user credentials
        demo_user, demo_password , demo_email = generate_random_credentials()

        # Create a demo user in the Django auth system
        try:
            new_user = User.objects.create_user(username=demo_user, password=demo_password, email=demo_email)
            new_user.save()
        except Exception as e:
            return JsonResponse({"error": "Error creating demo user" + str(e)}, status=500)
        
        return JsonResponse({
            "id": lead.id,
            "number": lead.number,
            "created_at": lead.created_at.isoformat(),
            "demo_user":demo_user,
            "demo_password":demo_password
        }, status=201)