import streamlit as st
import requests
import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# --- CONFIGURATION ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# --- 1. LOAD ALL STORES ---
@st.cache_data(ttl=3600)
def load_store_data():
    combined_data = []
    
    # Load Rimi
    try:
        with open("discounts.json", "r", encoding="utf-8") as f:
            rimi_data = json.load(f)
            for item in rimi_data:
                item['store'] = "Rimi"
                combined_data.append(item)
    except FileNotFoundError:
        pass

    # Load Maxima
    try:
        with open("discounts_maxima.json", "r", encoding="utf-8") as f:
            maxima_data = json.load(f)
            for item in maxima_data:
                item['store'] = "Maxima"
                combined_data.append(item)
    except FileNotFoundError:
        pass
        
    # Load Selver
    try:
        with open("discounts_selver.json", "r", encoding="utf-8") as f:
            selver_data = json.load(f)
            for item in selver_data:
                item['store'] = "Selver"
                combined_data.append(item)
    except FileNotFoundError:
        pass

    # Calculate discount percentages for ALL items
    for item in combined_data:
        if item['old_price'] > item['price'] and item['old_price'] > 0:
            item['discount_pct'] = ((item['old_price'] - item['price']) / item['old_price']) * 100
        else:
            item['discount_pct'] = 0
            
    return combined_data

# --- 2. AI DATA CLEANER ---
@st.cache_data(show_spinner=False) 
def ai_normalize_ingredient(estonian_name):
    prompt = f"""
    You are an expert culinary translator. The input is strictly in the ESTONIAN language.
    WARNING: Beware of false friends! The Estonian word "sea" or "sealiha" means "PORK" (pig), NOT the ocean/fish.
    
    RULE 1: If the product is NOT edible human food, reply with exactly: non-food
    RULE 2: If it IS human food, ignore the brand, weight, and packaging. Translate it to the core, generic English food ingredient.
    
    Product: {estonian_name}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0.0 
        )
        result = response.choices[0].message.content.strip().lower()
        if "non-food" in result or "unknown" in result:
            return None
        return result
    except Exception as e:
        st.error(f"AI Error: {e}")
        return None

# --- 3. RECIPE ENGINE (OpenAI Chef) ---
@st.cache_data(show_spinner=False)
def generate_custom_recipe(ingredients_list):
    prompt = f"""
    You are a creative, professional chef. I bought these discounted ingredients from the supermarket:
    {', '.join(ingredients_list)}

    Your job is to invent ONE delicious, cohesive recipe that uses ALL of these ingredients together in a single dish.
    Assume I already have basic pantry staples at home (cooking oil, salt, pepper, butter, basic spices, garlic, onion).

    Format your response beautifully in Markdown exactly like this:
    ### 🍽️ [Creative Name of the Dish]
    **You will also need to buy/have:** (Keep this list very short)
    
    **Instructions:**
    1. ...
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7, 
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"AI Chef Error: {e}")
        return None

# --- 4. FRONTEND UI ---
st.set_page_config(page_title="SäästuRetsept Haapsalu", layout="wide")

# 🚨 THE MAGIC FIX: Initialize a permanent memory for our cart and ingredients!
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'ingredients' not in st.session_state:
    st.session_state.ingredients = {}

st.title("🛒 Haapsalu SäästuRetsept")
st.write("Compare deals across Rimi, Maxima & Selver, and let AI cook your dinner!")

discounts = load_store_data()

# --- UI: SEARCH, FILTER, AND SORT ---
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    search_query = st.text_input("🔍 Search (e.g., 'kana', 'juust', 'kartul')").lower()

with col2:
    store_filter = st.selectbox("🏬 Select Store:", ["All Stores", "Rimi", "Maxima", "Selver"])

with col3:
    sort_option = st.selectbox("↕️ Sort Deals By:", ["Biggest Discount (%)", "Lowest Price (€)", "A-Z"])

if store_filter != "All Stores":
    discounts = [item for item in discounts if item.get('store') == store_filter]

if search_query:
    discounts = [item for item in discounts if search_query in item['name'].lower()]

if sort_option == "Biggest Discount (%)":
    discounts.sort(key=lambda x: x['discount_pct'], reverse=True)
elif sort_option == "Lowest Price (€)":
    discounts.sort(key=lambda x: x['price'])
elif sort_option == "A-Z":
    discounts.sort(key=lambda x: x['name'])

st.subheader(f"🔥 Displaying Top Deals ({len(discounts)} found)")

display_items = discounts[:80] 

st.write("") 
cols = st.columns(4) 
for index, item in enumerate(display_items):
    col = cols[index % 4]
    with col:
        st.container(border=True) 
        
        if item.get('image') and item['image'] != "🛒":
            st.image(item['image'], width=120)
        else:
            st.write(f"### 🛒")
            
        store_name = item.get('store', 'Unknown')
        if store_name == "Rimi":
            store_color = "🔴"
        elif store_name == "Maxima":
            store_color = "🔵"
        elif store_name == "Selver":
            store_color = "🟢"
        else:
            store_color = "⚪"
            
        st.caption(f"{store_color} **{store_name}**")
        st.write(f"**{item['name']}**")
        
        if item.get('discount_pct', 0) > 0:
            st.write(f"💰 **€{item['price']:.2f}** ~~(€{item['old_price']:.2f})~~ *( -{int(item['discount_pct'])}% )*")
        else:
            st.write(f"💰 **€{item['price']:.2f}**")
            
        unique_key = f"{item['name']}_{store_name}_{index}"
        
        # 🚨 NEW LOGIC: Check if this item is in our permanent memory
        is_in_cart = unique_key in st.session_state.cart
        
        # We set the checkbox state based on our memory!
        checked = st.checkbox(f"Add to Basket", value=is_in_cart, key=f"chk_{unique_key}")
        
        # If user checked it, add to memory
        if checked and not is_in_cart:
            st.session_state.cart[unique_key] = item
            with st.spinner("Translating..."):
                generic_name = ai_normalize_ingredient(item['name'])
                if generic_name:
                    st.session_state.ingredients[unique_key] = generic_name
                else:
                    st.warning("⚠️ AI flagged this as non-edible!")
                    
        # If user unchecked it, remove from memory
        elif not checked and is_in_cart:
            del st.session_state.cart[unique_key]
            if unique_key in st.session_state.ingredients:
                del st.session_state.ingredients[unique_key]

# Extract the lists from our permanent memory
cart_items = list(st.session_state.cart.values())
selected_ingredients = list(st.session_state.ingredients.values())

# --- UI: SIDEBAR SAVINGS TRACKER ---
st.sidebar.title("🛒 Your Basket")

if cart_items:
    total_price = sum(item['price'] for item in cart_items)
    total_old_price = sum(item['old_price'] for item in cart_items)
    total_saved = total_old_price - total_price
    
    st.sidebar.subheader("Order Summary")
    st.sidebar.write(f"**Total Cost:** €{total_price:.2f}")
    st.sidebar.write(f"~~Original Price: €{total_old_price:.2f}~~")
    
    if total_saved > 0:
        st.sidebar.success(f"🎉 **You Save: €{total_saved:.2f}!**")
        
    st.sidebar.divider()
    st.sidebar.write("**Items in basket:**")
    for cart_item in cart_items:
        s_name = cart_item.get('store')
        s_icon = "🔴" if s_name == "Rimi" else "🔵" if s_name == "Maxima" else "🟢"
        st.sidebar.caption(f"{s_icon} {cart_item['name']} (**€{cart_item['price']:.2f}**)")
else:
    st.sidebar.info("Your basket is empty. Select deals to see your savings!")

# --- UI: AI RECIPE GENERATION ---
if selected_ingredients:
    st.divider()
    
    if len(selected_ingredients) < 3:
        st.info(f"🛒 You have selected **{len(selected_ingredients)}** item(s): {', '.join(selected_ingredients).title()}.\n\n👉 **Please select at least {3 - len(selected_ingredients)} more item(s)** to let the AI Chef create a cohesive meal!")
    else:
        st.subheader("👨‍🍳 Your Custom Deal-to-Meal Recipe")
        st.write(f"The AI Chef is fusing together: **{', '.join(selected_ingredients).title()}**...")
        
        with st.spinner("Inventing your custom recipe..."):
            custom_recipe = generate_custom_recipe(selected_ingredients)
            
            if custom_recipe:
                with st.container(border=True):
                    st.markdown(custom_recipe)
            else:
                st.error("The Chef is taking a break. Please try again!")