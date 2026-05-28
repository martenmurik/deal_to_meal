import requests
import json
import time

def fetch_all_selver_discounts():
    print("🛒 Starting full ElasticSearch scrape of e-Selver...")

    cookies = {
    '_upscope__region': 'ImV1LWNlbnRyYWwi',
    'CookieConsent': '{stamp:%27SBunabEhcmytKWvIzrzU5jFKqy5aC7QjNt7xqCyH1xReLM/xhV5Tag==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1779728540389%2Cregion:%27ee%27}',
    '_upscope__shortId': 'IlpDWEZSTEtLQk5HMDFNVFlEIg==',
    }

    headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9,et;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjMwODE0OTkiLCJhcCI6IjI4NzQ0MjcyMyIsImlkIjoiMTFkNDgwOWI0YjM3MTI2ZCIsInRyIjoiOGYyODQyNTI4MWU1Y2Q5OWI5MzQyMTFhNTJhMzRiN2EiLCJ0aSI6MTc3OTcyOTU1NDc4MiwidGsiOiIyOTEyMTQ1In19',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.selver.ee/soodushinnaga-tooted/toidukaubad?page=2',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'traceparent': '00-8f28425281e5cd99b934211a52a34b7a-11d4809b4b37126d-01',
    'tracestate': '2912145@nr=0-1-3081499-287442723-11d4809b4b37126d----1779729554782',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    # 'cookie': '_upscope__region=ImV1LWNlbnRyYWwi; CookieConsent={stamp:%27SBunabEhcmytKWvIzrzU5jFKqy5aC7QjNt7xqCyH1xReLM/xhV5Tag==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1779728540389%2Cregion:%27ee%27}; _upscope__shortId=IlpDWEZSTEtLQk5HMDFNVFlEIg==',
    }

    url = 'https://www.selver.ee/api/catalog/vue_storefront_catalog_et/product/_search'

    unique_selver_items = {}
    
    # ElasticSearch pagination uses 'from' (starting item index) and 'size' (how many to grab)
    current_from = 0
    page_size = 96 # Let's be aggressive and grab 96 items at a time!
    
    # We explicitly ask for Category 366 (Food Deals)
    base_request_payload = {
        "query": {
            "bool": {
                "filter": {
                    "bool": {
                        "must": [
                            {"terms": {"visibility": [2, 3, 4]}},
                            {"terms": {"status": [0, 1]}},
                            {"terms": {"category_ids": [366]}}
                        ]
                    }
                }
            }
        },
        "sort": [{"category.position": {"order": "asc", "mode": "min", "nested_path": "category", "nested_filter": {"term": {"category.category_id": 366}}}}]
    }

    while True:
        print(f"📄 Scraping items {current_from} to {current_from + page_size}...")
        
        params = {
            '_source_exclude': 'configurable_options,product_nutr_info,product_nutr_unit,product_nutr_energy,product_nutr_fats,product_nutr_fats_acids,product_nutr_carbohydrates,product_nutr_sugars,product_nutr_proteins,product_nutr_salt,sgn,*.sgn,msrp_display_actual_price_type,*.msrp_display_actual_price_type,required_options',
            '_source_include': 'documents,activity,configurable_children.attributes,configurable_children.id,configurable_children.final_price,configurable_children.color,configurable_children.original_price,configurable_children.original_price_incl_tax,configurable_children.price,configurable_children.price_incl_tax,configurable_children.size,configurable_children.sku,configurable_children.special_price,configurable_children.special_price_incl_tax,configurable_children.tier_prices,final_price,id,image,name,new,original_price_incl_tax,original_price,price,price_incl_tax,product_links,sale,special_price,special_to_date,special_from_date,special_price_incl_tax,status,tax_class_id,tier_prices,type_id,url_path,url_key,*image,*sku,*small_image,short_description,manufacturer,product_*,extension_attributes.deposit_data,stock,product_stocktype,product_stocksource,prices,vmo_badges,product_nutr_energy_kcal',
            'from': str(current_from),
            'size': str(page_size),
            'sort': 'position:asc',
            'request': json.dumps(base_request_payload) # We convert our Python dictionary to a JSON string!
        }

        try:
            response = requests.get(url, params=params, cookies=cookies, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            # ElasticSearch stores results inside hits -> hits
            hits = data.get('hits', {}).get('hits', [])
            
            if not hits:
                print("🏁 No more items found. Scraping finished!")
                break
                
            for hit in hits:
                item = hit.get('_source', {})
                item_id = item.get('id')
                
                name = item.get('name', 'Unknown Item')
                
                # --- NEW PRICE LOGIC (With VAT Included) ---
                # 1. Get the standard base price (with tax)
                base_price = item.get('price_incl_tax') or item.get('price', 0.0)
                
                # 2. Check for a standard discount
                special_price = item.get('special_price_incl_tax')
                current_price = special_price if special_price else base_price
                
                # 3. Check for a Partner Card discount (Tier Prices override everything if cheaper)
                tier_prices = item.get('tier_prices', [])
                if tier_prices and len(tier_prices) > 0:
                    partner_price = tier_prices[0].get('value')
                    if partner_price and partner_price < current_price:
                        current_price = partner_price
                        
                # 4. Set the old price (Original price with tax, or the base price)
                old_price = item.get('original_price_incl_tax') or base_price
                
                # If it's not actually on sale, skip it!
                if old_price <= current_price:
                    continue
                # -------------------------------------------

                # Selver uses a CDN for images. We construct the full URL.
                image_path = item.get('image', '')
                image_url = f"https://www.selver.ee/img/800/800/resize{image_path}" if image_path else "🛒"
                
                if item_id:
                    unique_selver_items[item_id] = {
                        "name": name,
                        "price": current_price,
                        "old_price": old_price,
                        "image": image_url,
                        "store": "Selver" # Tag it!
                    }
            
            # Move the pagination index forward by 100
            current_from += page_size
            time.sleep(1.5)

        except Exception as e:
            print(f"❌ Error at index {current_from}: {e}")
            break

    final_list = list(unique_selver_items.values())
    
    with open("discounts_selver.json", "w", encoding="utf-8") as f:
        json.dump(final_list, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Successfully saved {len(final_list)} Selver deals!")

if __name__ == "__main__":
    fetch_all_selver_discounts()