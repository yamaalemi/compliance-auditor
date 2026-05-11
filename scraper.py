import pandas as pd
from playwright.sync_api import sync_playwright
from datetime import datetime

def run_scraper():
    print("🚀 Targeting NW8 - St John's Wood...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Direct link to Dexters St John's Wood Lettings
            url = 'https://www.dexters.co.uk/property-to-rent/property-in-st-johns-wood'
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # Dexters usually uses 'h3' or specific classes for addresses
            # We will grab all text that looks like a property title
            elements = page.locator('h3').all_inner_texts()
            
            # Filter for results that actually look like NW8 addresses
            addresses = [e.strip() for e in elements if "St John's Wood" in e or "NW8" in e]
            
            if addresses:
                df = pd.DataFrame({
                    'Address': addresses,
                    'Audit_Date': datetime.now().strftime("%Y-%m-%d"),
                    'Risk_Level': 'Checking...'
                })
                df.to_csv('database.csv', index=False)
                print(f"✅ Success! Found {len(addresses)} properties in NW8.")
            else:
                print("⚠️ No direct addresses found. Printing page content for debug:")
                print(page.content()[:500]) # Shows us if we are blocked
            
            browser.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_scraper()
