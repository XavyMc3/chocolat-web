import os
import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin

# Base URL for Para Ti
BASE_URL = "https://www.chocolatesparati.net/"

CATEGORIES = {
    "colecciones-premium": "https://www.chocolatesparati.net/categoria/chocolates-en-cajas/",
    "delicias-envueltas": "https://www.chocolatesparati.net/categoria/chocolates-in-bag/",
    "artesania-pura": "https://www.chocolatesparati.net/categoria/chocolates-in-handmade-boxes/",
    "tesoros-confitados": "https://www.chocolatesparati.net/categoria/dragees/",
    "tabletas-gourmet": "https://www.chocolatesparati.net/categoria/tablets/",
    "ediciones-especiales": "https://www.chocolatesparati.net/categoria/temporada/" # Corrected based on common wp structure or previous finding
}

# The browser found 'https://www.chocolatesparati.net/category/products/seasons/' in step 330, but let's stick to the /categoria/ ones if possible, or mixed.
# Actually, let's use the ones verified by the browser subagent where possible.
# Browser verified: "https://www.chocolatesparati.net/categoria/chocolates-in-handmade-boxes/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Referer": "https://www.chocolatesparati.net/",
    "Connection": "keep-alive"
}

# Directory to save images
IMAGE_DIR = "../public/images/products/parati"

def download_image(url, category, filename):
    folder = os.path.join(IMAGE_DIR, category)
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        return path
    
    try:
        response = requests.get(url, headers=HEADERS, stream=True)
        if response.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return path
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return None

def scrape_category(url, category_name):
    print(f"Scraping category: {category_name}...")
    products = []
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to load {url}")
            return products

        soup = BeautifulSoup(response.text, 'html.parser')
        product_items = soup.select('li.product')

        for item in product_items:
            title_tag = item.select_one('h2.woocommerce-loop-product__title')
            img_tag = item.select_one('img')
            link_tag = item.select_one('a.woocommerce-LoopProduct-link')

            if title_tag and img_tag:
                name = title_tag.get_text(strip=True)
                img_url = img_tag.get('src')
                product_url = link_tag.get('href') if link_tag else None
                
                # Sanitize filename
                filename = name.lower().replace(" ", "_").replace("/", "-") + ".jpg"
                save_path = download_image(img_url, category_name, filename)
                
                # Relative path for Astro project
                relative_path = f"/images/products/parati/{category_name}/{filename}"

                products.append({
                    "name": name,
                    "image": relative_path,
                    "brand": "Para Ti",
                    "category": category_name,
                    "description": "", # We could scrape detail page but let's start simple
                    "price": 0, # Usually not on list
                    "badge": None
                })
                print(f"  Captured: {name}")

    except Exception as e:
        print(f"Error in category {category_name}: {e}")
    
    return products

def main():
    all_products = {}
    
    for cat_name, url in CATEGORIES.items():
        products = scrape_category(url, cat_name)
        all_products[cat_name] = products
        time.sleep(1) # Be polite

    # Save metadata
    with open('scraped_products.json', 'w', encoding='utf-8') as f:
        json.dump(all_products, f, ensure_ascii=False, indent=2)
    
    print("Scraping complete. Results saved to scraped_products.json")

if __name__ == "__main__":
    main()
