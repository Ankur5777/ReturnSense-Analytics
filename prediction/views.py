import os
import joblib
import pandas as pd
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.decorators import login_required

from .models import OrderPrediction

# ----------------------------------------------------
# 1. Model Loading
# ----------------------------------------------------
MODEL_PATH = os.path.join(settings.BASE_DIR, 'return_prediction_pipeline.joblib')

try:
    model = joblib.load(MODEL_PATH)
    print(f"[SUCCESS] ML Pipeline loaded successfully from: {MODEL_PATH}")
except Exception as e:
    model = None
    print(f"[ERROR] Could not load model pipeline: {e}")


# ----------------------------------------------------
# 2. Authentication Views
# ----------------------------------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    error_message = None
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')

        user = authenticate(request, username=username_input, password=password_input)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('home')
        else:
            error_message = "Invalid username or password. Please try again."

    return render(request, 'prediction/login.html', {'error': error_message})


def logout_view(request):
    logout(request)
    return redirect('login')


# ----------------------------------------------------
# 3. Protected Application Views
# ----------------------------------------------------
@login_required
def home(request):
    return render(request, 'prediction/home.html')


@login_required
def dashboard(request):
    context = {
        'total_orders': '384,873',
        'overall_return_rate': '48.3%',
        'avg_delivery_days': '5.8',
        'bracketing_rate': '7.5%',
        'price_labels': ['Low (< €35)', 'Medium (€35-€60)', 'High (€60-€90)', 'Premium (> €90)'],
        'price_returns': [44.1, 47.3, 51.2, 53.6],
        'delay_labels': ['1-2 Days', '3-4 Days', '5-6 Days', '7-9 Days', '10-14 Days', '15+ Days'],
        'delay_returns': [42.0, 45.4, 48.1, 53.7, 58.2, 63.9],
        'sizing_labels': ['Fitted Apparel', 'Unsized / Accessories'],
        'sizing_rates': [50.4, 28.1],
        'mfg_labels': ['Mfg 20', 'Mfg 11', 'Mfg 14', 'Mfg 1', 'Mfg 46', 'Mfg 37', 'Mfg 3'],
        'mfg_rates': [59.6, 56.8, 52.2, 51.8, 48.7, 44.8, 38.8],
    }
    return render(request, 'prediction/dashboard.html', context)


@login_required
def predict(request):
    result = None

    if request.method == 'POST':
        try:
            price = float(request.POST.get('price', 59.9))
            manufacturer_id = int(request.POST.get('manufacturerID', 1))
            delivery_duration = int(request.POST.get('delivery_duration', 4))
            is_delivery_missing = 1 if request.POST.get('is_delivery_missing') else 0
            customer_age = float(request.POST.get('customer_age', 35))
            account_age_days = int(request.POST.get('account_age_days', 120))
            order_month = int(request.POST.get('order_month', 6))
            is_bracketed = 1 if request.POST.get('is_bracketed') else 0
            is_unsized = 1 if request.POST.get('is_unsized') else 0
            salutation = str(request.POST.get('salutation', 'Mrs'))
            state = str(request.POST.get('state', 'Bavaria'))
            order_day_of_week = str(request.POST.get('order_day_of_week', 'Monday'))

            # Prepare 1-row DataFrame matching the model's feature names
            input_data = pd.DataFrame([{
                'price': price,
                'manufacturerID': manufacturer_id,
                'delivery_duration': delivery_duration,
                'is_delivery_missing': is_delivery_missing,
                'customer_age': customer_age,
                'account_age_days': account_age_days,
                'order_month': order_month,
                'is_bracketed': is_bracketed,
                'is_unsized': is_unsized,
                'salutation': salutation,
                'state': state,
                'order_day_of_week': order_day_of_week
            }])

            # Run inference
            if model is not None:
                raw_probs = model.predict_proba(input_data)
                proba = float(raw_probs[0, 1])
                pred_class = 1 if proba >= 0.50 else 0
            else:
                proba = 0.50
                pred_class = 0

            percent = round(proba * 100, 1)
            pred_label = 'High Return Risk' if pred_class == 1 else 'Likely to Keep'

            # Persist record
            OrderPrediction.objects.create(
                price=price,
                manufacturer_id=manufacturer_id,
                delivery_duration=delivery_duration,
                is_delivery_missing=bool(is_delivery_missing),
                customer_age=customer_age,
                account_age_days=account_age_days,
                order_month=order_month,
                salutation=salutation,
                state=state,
                order_day_of_week=order_day_of_week,
                is_bracketed=bool(is_bracketed),
                is_unsized=bool(is_unsized),
                prediction_label=pred_label,
                return_probability=percent,
                is_high_risk=(pred_class == 1)
            )

            result = {
                'prediction': pred_label,
                'probability': percent,
                'is_return': (pred_class == 1),
                'inputs': request.POST
            }

        except (ValueError, TypeError) as parse_err:
            result = {'error': f"Invalid form submission: {parse_err}"}

    return render(request, 'prediction/prediction.html', {'result': result})


@login_required
def history(request):
    predictions = OrderPrediction.objects.all().order_by('-id')[:50]
    return render(request, 'prediction/history.html', {'predictions': predictions})


def custom_404_view(request, exception=None):
    return render(request, 'prediction/404.html', status=404)