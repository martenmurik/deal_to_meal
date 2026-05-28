import requests

def get_rimi_categories():
    print("🔍 Fetching Rimi Category Tree...\n")
    url = 'https://www.rimi.ee/epood/api/v1/content/category-tree'
    params = {'locale': 'ee'}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        for category in data.get('categories',[]):
            name = category.get('name', 'Unknown')
            # Extract the 'SH-XX' code from the end of the URL
            cat_url = category.get('url', '')
            cat_id = cat_url.split('/')[-1] if '/' in cat_url else 'Unknown ID'
            
            print(f"{cat_id} = {name}")
            
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    get_rimi_categories()