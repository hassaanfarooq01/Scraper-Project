import re
import time
import urllib.parse
from bs4 import BeautifulSoup
from celery import shared_task
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.db import transaction
from .models import Brand, Product
import logging

logger = logging.getLogger(__name__)


    
@shared_task
def scrape_all_brands_task():
    logger.info("Starting scrape_all_brands_task")
    brands = Brand.objects.filter(scraping_active=True)
    if not brands.exists():
        print("No Brands")

    for brand in brands:
        logger.info(f"Dispatching scraping for brand: {brand.name}")
        scrape_products_for_brand.delay(brand.name)
    logger.info("Completed scrape_all_brands_task")

def reset_scraping_status():
    """Sets scraping_active=False for all brands on server refresh or if no brand is searched."""
    Brand.objects.update(scraping_active=False)

@shared_task    
def scrape_products_for_brand(brand_name, *args, **kwargs):
    print("kwargs:: ", kwargs)
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage") 
    options.add_argument("--disable-gpu")  
    options.add_argument("--headless")
    options.add_argument("--window-size=1920x1080")  
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--remote-debugging-port=9222")  

    chrome_driver_path = '/usr/local/bin/chromedriver-linux64/chromedriver'
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    encoded_search_term = urllib.parse.quote_plus(brand_name)
    brand_url = f"https://www.amazon.com/s?k={encoded_search_term}"


    try:
        driver.get(brand_url)
        driver.refresh()
        time.sleep(3)

        current_page = 0
        while current_page <= 7:
            current_page += 1
            driver.get(f"{brand_url}&page={current_page}")
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-component-type="s-search-result"]'))
            )

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            product_listings = soup.find_all('div', {'data-component-type': 's-search-result'})

            if not product_listings:
                break

            for product in product_listings:
                product_name_element = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}) \
                      or product.find('span', {'class': 'a-text-normal'}) \
                      or product.find('h2', {'class': 'a-size-mini a-spacing-none a-color-base s-line-clamp-2'})
                product_name = product_name_element.text.strip() if product_name_element else None
                print('Product Name:',product_name)

                product_link_element = product.find('a', {'class': 'a-link-normal s-no-outline'})
                product_link = f"https://www.amazon.com{product_link_element['href']}" if product_link_element else None

                product_image_element = product.find('img', {'class': 's-image'})
                image_url = product_image_element['src'] if product_image_element else None

                asin = None
                if product_link:
                    asin_match = re.search(r'/dp/([A-Z0-9]{10})', product_link)
                    if asin_match:
                        asin = asin_match.group(1)
                        print(f"ASIN extracted from product link: {asin}")
                
                try:
                    driver.get(product_link)
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.ID, 'detailBullets_feature_div'))
                    )
                    product_page_soup = BeautifulSoup(driver.page_source, 'html.parser')
                    product_info_section = product_page_soup.find('div', {'id': 'detailBulletsWrapper_feature_div'})
                    if product_info_section:
                        asin_text = product_info_section.find(string=lambda text: 'ASIN' in text)
                        if asin_text:
                            asin = asin_text.find_next('span').text.strip()
                            print(f"ASIN found on page: {asin}")

                except Exception as e:
                    print(f"Error fetching ASIN from product page: {e}")

                
                if product_name and asin:
                    with transaction.atomic():
                        product_obj, created = Product.objects.update_or_create(
                            asin=asin,
                            brand=brand,
                            defaults={
                                'name': product_name,
                                'image': image_url
                            }
                        )

    except Exception as e:
        print(f"Error during scraping for {brand_name}: {e}")
    finally:
        driver.quit()
reset_scraping_status()