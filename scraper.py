import pandas as pd
from playwright.sync_api import sync_playwright
from datetime import datetime
import time

def run_scraper():
    with sync_playwright() as p:
        # Launch browser with specific 'Stealth' settings
        browser = p.chromium.launch(headless=True)
        
        # We use a 'Context' to make the bot look like a real Mac user
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        # 1. Target URL (Rightmove Manchester)
        print("🚀 Visiting Rightmove...")
        url = 'https://www.rightmove.co.uk/property-to-rent/find.html?searchLocation=Manchester'
        page.goto(url, wait_until="domcontentloaded")
        
        # 2. Add a 'Human' pause so we aren't too fast
        time.sleep(5) 
        
        # 3. New 2026 Selector: Rightmove hides addresses in 'propertyCard-address'
        print("🔍 Searching for addresses...")
        elements = page.query_selector_all('.propertyCard-address')
        
        addresses = [el.inner_text().strip() for el in elements if el.inner_text()]
        
        # 4. Save results
        if addresses:
            df = pd.DataFrame({
                'Address': list(set(addresses)), # Remove duplicates
                'Audit_Date': datetime.now().strftime("%Y-%m-%d"),
                'Risk_Level': 'High'
            })
            df.to_csv('database.csv', index=False)
            print(f"✅ Success! Found {len(addresses)} unique properties.")
        else:
            # If it fails, save a 'Check' file so we know the bot at least reached the site
            print("❌ No addresses found. The site might be blocking us.")
            
        browser.close()

if __name__ == "__main__":
    run_scraper()
