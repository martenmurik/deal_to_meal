import requests
import json
import time
from bs4 import BeautifulSoup

def fetch_all_rimi_discounts():
    print("🛒 Starting full scrape of Rimi e-pood...")

    # ---> PASTE YOUR WORKING COOKIES AND HEADERS HERE <---
    cookies = {
    '__uzma': '059f033d-1ada-4ae7-981a-b97586e7e32d',
    '__uzmb': '1778511887',
    '__uzme': '6047',
    '__ssds': '0',
    '__ssuzjsr0': 'a9be0cd8e',
    '__uzmaj0': 'b086fa18-584b-4a4b-ac8a-8d847f2cf062',
    '__uzmbj0': '1778511889',
    '__uzmlj0': 'mhpO6z7Sllc/eM19qnJKnNvG1g3Cz3O54sTXUmHm96k=',
    'XSRF-TOKEN': 'eyJpdiI6IlJISTdIbGFaeWtPdStVS2JZdE51SEE9PSIsInZhbHVlIjoibk1oRG9SVlpJZWpVTnhjYlV5NCs3MnVqL0dnUGNjdjlhR1VDVDN1SDNtdUoveW5RdEQrV0p1OEgxSFAzM2V6TUI1TkFhaC95b09YMU55aUdqQjhpYlZhUDdlck5FV0Z4Qko1WWtSL2FjK3d6U3ZTWWdabjc0S3c5K2E1aTVkSVYiLCJtYWMiOiJjNzY2NDg5ZmNkYjg3YmM2MjMxNDcyNTk3YmNiNDg1NDI1MTEwMzA3MDVjZDM0YjVmYjkyN2RlODI5ZDc3NmNmIiwidGFnIjoiIn0%3D',
    '__uzmcj0': '583953795272',
    '__uzmdj0': '1778518328',
    '__uzmfj0': '7f9000b086fa18-584b-4a4b-ac8a-8d847f2cf0621-17785118893736439570-0007db50d03bff4500537',
    'uzmxj': '7f900061b45d65-ed4a-4ad9-8426-6cd1540844f81-17785118893736439570-17cccbc818f9ea9f37',
    '__uzmd': '1778518329',
    '__uzmc': '6782755027297',
    'rimi_storefront_session': 'eyJpdiI6IlFFcHFnTS8xMG9MNnduZEdBVU9FRmc9PSIsInZhbHVlIjoibXBxR05vbFNKdG85QkJYNFlRRDRjVVc2SmM4b1BSY3l5T1dBazFlVjNKZ2RLcW0zTHdkNU1yVTEzQWFiaVNlWkpmdzhyUjg3U09TN2cwb0Rrek1YbmtXRHVOa0VvSWFVR1FGdDZmOEI0ck42MUF5aUs1SGhEbG1LSWwxY0xPUTIiLCJtYWMiOiJlZDE4OWE0ZDVmYTkwYjE0ZWNmNDk2NTAzZGZiYWVkN2Q4YzUwMWZiMDVhY2IyNmFhNTdlOGMwNzE2OTQ1NDFlIiwidGFnIjoiIn0%3D',
    }

    headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9,et;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.rimi.ee/epood/ee/parimad-pakkumised?currentPage=2&pageSize=40',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'uzlc': '7f9000b086fa18-584b-4a4b-ac8a-8d847f2cf0621-17785118893734531716-000393414f314abf9aa31100215087942HgoVOb086fa18',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': '__uzma=059f033d-1ada-4ae7-981a-b97586e7e32d; __uzmb=1778511887; __uzme=6047; __ssds=0; __ssuzjsr0=a9be0cd8e; __uzmaj0=b086fa18-584b-4a4b-ac8a-8d847f2cf062; __uzmbj0=1778511889; __uzmlj0=mhpO6z7Sllc/eM19qnJKnNvG1g3Cz3O54sTXUmHm96k=; XSRF-TOKEN=eyJpdiI6IlJISTdIbGFaeWtPdStVS2JZdE51SEE9PSIsInZhbHVlIjoibk1oRG9SVlpJZWpVTnhjYlV5NCs3MnVqL0dnUGNjdjlhR1VDVDN1SDNtdUoveW5RdEQrV0p1OEgxSFAzM2V6TUI1TkFhaC95b09YMU55aUdqQjhpYlZhUDdlck5FV0Z4Qko1WWtSL2FjK3d6U3ZTWWdabjc0S3c5K2E1aTVkSVYiLCJtYWMiOiJjNzY2NDg5ZmNkYjg3YmM2MjMxNDcyNTk3YmNiNDg1NDI1MTEwMzA3MDVjZDM0YjVmYjkyN2RlODI5ZDc3NmNmIiwidGFnIjoiIn0%3D; __uzmcj0=583953795272; __uzmdj0=1778518328; __uzmfj0=7f9000b086fa18-584b-4a4b-ac8a-8d847f2cf0621-17785118893736439570-0007db50d03bff4500537; uzmxj=7f900061b45d65-ed4a-4ad9-8426-6cd1540844f81-17785118893736439570-17cccbc818f9ea9f37; __uzmd=1778518329; __uzmc=6782755027297; rimi_storefront_session=eyJpdiI6IlFFcHFnTS8xMG9MNnduZEdBVU9FRmc9PSIsInZhbHVlIjoibXBxR05vbFNKdG85QkJYNFlRRDRjVVc2SmM4b1BSY3l5T1dBazFlVjNKZ2RLcW0zTHdkNU1yVTEzQWFiaVNlWkpmdzhyUjg3U09TN2cwb0Rrek1YbmtXRHVOa0VvSWFVR1FGdDZmOEI0ck42MUF5aUs1SGhEbG1LSWwxY0xPUTIiLCJtYWMiOiJlZDE4OWE0ZDVmYTkwYjE0ZWNmNDk2NTAzZGZiYWVkN2Q4YzUwMWZiMDVhY2IyNmFhNTdlOGMwNzE2OTQ1NDFlIiwidGFnIjoiIn0%3D',
    }

    url = 'https://www.rimi.ee/epood/ee/parimad-pakkumised'
    
    # MAGICAL FIX: Using a dictionary prevents ANY duplicates from ever being saved!
    unique_items = {}
    current_page = 1
    previous_page_ids =[]

    # 🚨 THE NUCLEAR OPTION: Rimi's Internal Food Category IDs 🚨
    # SH-1: Groceries, SH-2: Bakery, SH-8: Meat/Fish, SH-9: Ready Meals, 
    # SH-11: Dairy/Eggs, SH-12: Fruits/Veggies, SH-13: Frozen, SH-14: Drinks, 
    # SH-15: Snacks, SH-16: Vegan/Diet, SH-19: Local Farm, SH-20: Party food
    ALLOWED_FOOD_CATEGORIES = (
        'SH-3-', 'SH-4-', 'SH-6-', 'SH-8-', 'SH-9-', 'SH-11-', 
        'SH-12-', 'SH-13-', 'SH-16-', 'SH-17-', 'SH-19-', 'SH-20-'
    )

    while True:
        print(f"📄 Scraping Page {current_page}...")
        
        params = {
            'currentPage': str(current_page),
            'pageSize': '80', 
            'query': ''
        }
        
        headers['x-requested-with'] = 'XMLHttpRequest'
        headers['accept'] = 'application/json'

        try:
            response = requests.get(url, params=params, cookies=cookies, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            html_content = data.get('products', '')
            soup = BeautifulSoup(html_content, 'html.parser')
            
            product_divs = soup.find_all('div', class_='js-product-container')
            
            if not product_divs:
                break
                
            current_page_ids =[]
            
            for div in product_divs:
                product_json_str = div.get('data-gtm-eec-product')
                
                if product_json_str:
                    product_info = json.loads(product_json_str)
                    
                    # Grab the ID and the Category!
                    item_id = product_info.get('id')
                    category = product_info.get('category', '')
                    
                    # 🚨 THE VIP BOUNCER: If it's not food, SKIP IT completely!
                    if not category.startswith(ALLOWED_FOOD_CATEGORIES):
                        continue
                    
                    name = product_info.get('name', 'Unknown Item')
                    base_price = product_info.get('price', 0.0) 
                    
                    current_page_ids.append(item_id)
                    current_price = base_price
                    old_price = base_price
                    
                    # 1A. LOYALTY PRICE
                    major_span = div.select_one('.price-label__price .major')
                    cents_span = div.select_one('.price-label__price .cents')
                    if major_span and cents_span:
                        current_price = float(f"{major_span.text.strip()}.{cents_span.text.strip()}")
                    else:
                        # 1B. STANDARD PRICE
                        std_major = div.select_one('.card__price span[aria-hidden="true"]')
                        std_cents = div.select_one('.card__price sup')
                        if std_major and std_cents:
                            current_price = float(f"{std_major.text.strip()}.{std_cents.text.strip()}")

                    # 1C. OLD PRICE
                    old_price_span = div.select_one('.card__old-price span[aria-hidden="true"]')
                    if old_price_span:
                        import re
                        old_p_str = re.sub(r'[^\d,.-]', '', old_price_span.text).replace(',', '.')
                        try:
                            old_price = float(old_p_str)
                        except:
                            pass

                    # 2. HD IMAGE
                    image_url = "🛒" 
                    img_tag = div.select_one('.card__image-wrapper img')
                    if img_tag:
                        image_url = img_tag.get('data-src') or img_tag.get('src') or "🛒"
                        image_url = image_url.replace('q_auto:low', 'q_100').replace('q_1', 'q_100').replace('h_216', 'h_600').replace('w_216', 'w_600')

                    # 3. SAVE
                    if item_id:
                        unique_items[item_id] = {
                            "name": name,
                            "price": current_price,
                            "old_price": old_price,
                            "image": image_url
                        }
                        
            # Duplicate Page Protection
            if not current_page_ids or current_page_ids == previous_page_ids:
                print("🏁 Pages started repeating. We have grabbed everything!")
                break
                
            previous_page_ids = current_page_ids
            
            current_page += 1
            time.sleep(1.5)

        except Exception as e:
            print(f"❌ Error on page {current_page}: {e}")
            break

    final_list = list(unique_items.values())
    
    with open("discounts.json", "w", encoding="utf-8") as f:
        json.dump(final_list, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Successfully saved {len(final_list)} PURE FOOD items to discounts.json!")

if __name__ == "__main__":
    fetch_all_rimi_discounts()