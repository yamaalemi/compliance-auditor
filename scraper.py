import pandas as pd
from playwright.sync_api import sync_playwright
from datetime import datetime

def run_scraper():
    print("🚀 Starting Stealth Scraper...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            # Use a very specific mobile user agent (easier to bypass blocks)
            context = browser.new_context(user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1")
            page = context.new_page()
            
            # Target URL
            url = 'https://www.rightmove.co.uk/property-to-rent/find.html?searchLocation=Manchester'
            print(f"📡 Navigating to: {url}")
            
            page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Just grab the page title to see if we got blocked
            print(f"📄 Page Title: {page.title()}")
            
            # Try to find any text that looks like a postcode or address
            elements = page.locator('.propertyCard-address').all_inner_texts()
            
            if elements:
                df = pd.DataFrame({
                    'Address': [e.strip() for e in elements],
                    'Audit_Date': datetime.now().strftime("%Y-%m-%d"),
                    'Risk_Level': 'High'
                })
                df.to_csv('database.csv', index=False)
                print(f"✅ Found {len(elements)} properties.")
            else:
                print("⚠️ No properties found on page. Might be a captcha.")
                # Create an empty file so the next step doesn't crash
                with open('database.csv', 'w') as f:
                    f.write("Address,Audit_Date,Risk_Level\nNo Data,Found,Today")
            
            browser.close()
    except Exception as e:
        print(f"❌ Script Error: {e}")
        with open('database.csv', 'w') as f:
            f.write("Address,Audit_Date,Risk_Level\nError,Occurred,Check Logs")

if __name__ == "__main__":
    run_scraper()
