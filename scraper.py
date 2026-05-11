import pandas as pd
from playwright.sync_api import sync_playwright
from datetime import datetime

def run_scraper():
    with sync_playwright() as p:
        # Launch browser with a "Human-like" user agent
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()
        
        # 1. Target URL (Rightmove Manchester example)
        # TIP: Make sure this is a search result page
        url = 'https://www.rightmove.co.uk/property-to-rent/find.html?searchLocation=Manchester'
        page.goto(url, wait_until="networkidle")
        
        # 2. Wait for the properties to actually appear on screen
        page.wait_for_selector('address', timeout=10000)
        
        # 3. Extract addresses using a more robust selector
        # Rightmove 2026 often uses 'address' tags or specific classes
        addresses = page.locator('address').all_inner_texts()
        
        if not addresses:
            print("❌ No addresses found. Trying alternative selector...")
            addresses = page.locator('.propertyCard-address').all_inner_texts()

        # 4. Clean and Save
        if addresses:
            df = pd.DataFrame({
                'Address': [a.strip() for a in addresses],
                'Audit_Date': datetime.now().strftime("%Y-%m-%d"),
                'Risk_Level': 'Checking...'
            })
            df.to_csv('database.csv', index=False)
            print(f"✅ Success! Found {len(addresses)} properties.")
        else:
            print("❌ Still no data. Agent might be blocking the request.")
            
        browser.close()

if __name__ == "__main__":
    run_scraper()
