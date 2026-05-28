import requests
import json
import time
import re

def fetch_all_maxima_discounts():
    print("🛒 Starting full HTML-state scrape of Barbora (Maxima)...")

    cookies = {
    'CookieConsent': '{stamp:%27g9aBuqvdiAyUypxiWIHQim4xKwAn0x+WwswMPlBTQ4CNIYv1+ojrKw==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1778787500118%2Cregion:%27ee%27}',
    'X-Session-ID': '28ce105f-eca7-4781-a91a-c8316429e998',
    'BN-Checkout-Test-Group': 'true',
    'ConstructorioID_session_id': '1',
    'ConstructorioID_client_id': 'a3dd6dd0-267a-44c6-8d35-0bec0db92f1c',
    'ConstructorioID_session': '{"sessionId":1,"lastTime":1778791115779}',
    'AWSALBTG': 'YcSb+a9FjRA6U7u7OU/2Kq9pkzc27Jjv7CmKiDQa0zk5lTgevPp4T0+HEPrv+xDIhqDPJbdZwe+V/smaZfp1/aAJX2CxmU0En47e/q0FQ1VdyFMV+oXJXpxbgnlOu6huwXoNjveqnvWV+8p1i+6g/H5YOXhNzv2yejBGbAv5eXMe',
    'AWSALBTGCORS': 'YcSb+a9FjRA6U7u7OU/2Kq9pkzc27Jjv7CmKiDQa0zk5lTgevPp4T0+HEPrv+xDIhqDPJbdZwe+V/smaZfp1/aAJX2CxmU0En47e/q0FQ1VdyFMV+oXJXpxbgnlOu6huwXoNjveqnvWV+8p1i+6g/H5YOXhNzv2yejBGbAv5eXMe',
    'AWSALB': 'jaizLFt8kIp90R6je0d6sTPKR//RJd9B8tsc5rcVrZGszx1YYrxrtk5SA58vZF0XLAP1pDIDYQ3KgedSTC5WB95k40bHPcnI4+/a18CsEevxA6YXfy/e08WrPPZO',
    'AWSALBCORS': 'jaizLFt8kIp90R6je0d6sTPKR//RJd9B8tsc5rcVrZGszx1YYrxrtk5SA58vZF0XLAP1pDIDYQ3KgedSTC5WB95k40bHPcnI4+/a18CsEevxA6YXfy/e08WrPPZO',
    }

    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,et;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://barbora.ee/pakkumised?page=2',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    # 'cookie': 'CookieConsent={stamp:%27g9aBuqvdiAyUypxiWIHQim4xKwAn0x+WwswMPlBTQ4CNIYv1+ojrKw==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1778787500118%2Cregion:%27ee%27}; X-Session-ID=28ce105f-eca7-4781-a91a-c8316429e998; BN-Checkout-Test-Group=true; ConstructorioID_session_id=1; ConstructorioID_client_id=a3dd6dd0-267a-44c6-8d35-0bec0db92f1c; ConstructorioID_session={"sessionId":1,"lastTime":1778791115779}; AWSALBTG=YcSb+a9FjRA6U7u7OU/2Kq9pkzc27Jjv7CmKiDQa0zk5lTgevPp4T0+HEPrv+xDIhqDPJbdZwe+V/smaZfp1/aAJX2CxmU0En47e/q0FQ1VdyFMV+oXJXpxbgnlOu6huwXoNjveqnvWV+8p1i+6g/H5YOXhNzv2yejBGbAv5eXMe; AWSALBTGCORS=YcSb+a9FjRA6U7u7OU/2Kq9pkzc27Jjv7CmKiDQa0zk5lTgevPp4T0+HEPrv+xDIhqDPJbdZwe+V/smaZfp1/aAJX2CxmU0En47e/q0FQ1VdyFMV+oXJXpxbgnlOu6huwXoNjveqnvWV+8p1i+6g/H5YOXhNzv2yejBGbAv5eXMe; AWSALB=jaizLFt8kIp90R6je0d6sTPKR//RJd9B8tsc5rcVrZGszx1YYrxrtk5SA58vZF0XLAP1pDIDYQ3KgedSTC5WB95k40bHPcnI4+/a18CsEevxA6YXfy/e08WrPPZO; AWSALBCORS=jaizLFt8kIp90R6je0d6sTPKR//RJd9B8tsc5rcVrZGszx1YYrxrtk5SA58vZF0XLAP1pDIDYQ3KgedSTC5WB95k40bHPcnI4+/a18CsEevxA6YXfy/e08WrPPZO',
    }
    
    urls_to_scrape = [
        'https://barbora.ee/pakkumised',
        'https://barbora.ee/aitah-hind'
    ]

    unique_maxima_items = {}

    # 🚨 THE MAXIMA BOUNCER: We ban their non-food categories!
    BANNED_CATEGORIES = [
        "puhastustarbed", "enesehooldustooted", "kodukaubad", "lastekaubad", "lemmiklooma"
    ]

    for url in urls_to_scrape:
        section_name = url.split('/')[-1].upper()
        print(f"\n🚀 Switching to section: {section_name}")
        
        current_page = 1
        previous_page_ids = []

        while True:
            print(f"📄 Scraping {section_name} - Page {current_page}...")
            
            params = {'page': str(current_page)}

            try:
                response = requests.get(url, params=params, cookies=cookies, headers=headers)
                response.raise_for_status()
                
                match = re.search(r'window\.b_productList\s*=\s*(\[.*?\])\s*;', response.text)
                
                if not match:
                    print(f"🏁 Couldn't find the product list. End of {section_name}!")
                    break
                    
                products_json_str = match.group(1)
                products = json.loads(products_json_str)
                
                if not products:
                    break
                    
                current_page_ids = []
                
                for item in products:
                    item_id = item.get('id')
                    if item_id:
                        current_page_ids.append(item_id)

                    category_path = item.get('category_name_full_path', '').lower()
                    
                    is_food = True
                    for banned_word in BANNED_CATEGORIES:
                        if banned_word in category_path:
                            is_food = False
                            break
                            
                    if not is_food:
                        continue 
                        
                    name = item.get('title', 'Unknown Item')
                    current_price = item.get('price', 0.0)
                    
                    old_price = item.get('retail_price')
                    
                    if not old_price or old_price <= current_price:
                        continue
                        
                    image_url = item.get('big_image') or item.get('image') or "🛒"
                    
                    if item_id:
                        unique_maxima_items[item_id] = {
                            "name": name,
                            "price": current_price,
                            "old_price": old_price,
                            "image": image_url,
                            "store": "Maxima" 
                        }
                
                if not current_page_ids or current_page_ids == previous_page_ids:
                    print(f"🏁 Pages started repeating. We grabbed all of {section_name}!")
                    break
                    
                previous_page_ids = current_page_ids
                current_page += 1
                time.sleep(1.5)

            except Exception as e:
                print(f"❌ Error on page {current_page}: {e}")
                break

    # After checking ALL URLs, save the final combined list
    final_list = list(unique_maxima_items.values())
    with open("discounts_maxima.json", "w", encoding="utf-8") as f:
        json.dump(final_list, f, ensure_ascii=False, indent=4)
        
    print(f"\n✅ Successfully saved {len(final_list)} TOTAL unique food deals from Maxima!")

if __name__ == "__main__":
    fetch_all_maxima_discounts()