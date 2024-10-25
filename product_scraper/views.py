from django.http import JsonResponse
from .tasks import scrape_products_for_brand
from django.views.decorators.csrf import csrf_exempt
from .models import Brand
import json
from django.shortcuts import render

def scrape_brand_products(request, brand_name):
    try:
        scrape_products_for_brand(brand_name)
        return JsonResponse({'status': 'Scraping started'}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)
    
@csrf_exempt
def scrape_brand_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            brand_name = data.get('brand_name')

            if not brand_name:
                return JsonResponse({'status': 'Error', 'message': 'Brand name is required.'}, status=400)

            # Trigger the scraping function for the provided brand
            scrape_products_for_brand.delay(brand_name)

            return JsonResponse({'status': 'Success', 'message': f'Scraping started for brand {brand_name}.'})

        except Exception as e:
            return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'Error', 'message': 'Only POST requests are allowed.'}, status=405)

def scrape_brand_page(request):
    return render(request, 'scrape_brand.html')
