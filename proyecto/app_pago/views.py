from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import mercadopago

@csrf_exempt  # Exenta la vista del control CSRF para pruebas
def pagar(request):
    if request.method == 'POST':
        mp = mercadopago.MP(settings.MERCADOPAGO_CLIENT_ID, settings.MERCADOPAGO_CLIENT_SECRET)
        preference_data = {
            "items": [
                {
                    "title": "Producto",
                    "quantity": 1,
                    "currency_id": "ARS",  # Cambia a una moneda admitida
                    "unit_price": 100.00,  # Asegúrate de que sea un número flotante
                }
            ]
        }
        preference = mp.create_preference(preference_data)
        if 'id' in preference['response']:
            return JsonResponse({'id': preference['response']['id']})
        else:
            return JsonResponse({'error': preference['response']}, status=400)
    return render(request, 'pagar.html')
