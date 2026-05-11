import pandas as pd
from playwright.sync_api import sync_playwright
from datetime import datetime

def run_scraper():
    with sync_playwright() as p:
        # 1. Launch the robot
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 2. Go to a local agent's page (Example: Manchester Rent)
        # You can change this URL later to any agent you want to audit
        page.goto('https://www.rightmove.co.uk/property-to-rent/find.html?searchLocation=Manchester')
        
        # 3. Grab property addresses
        addresses = page.locator('address').all_inner_texts()
        
        # 4. Save to a simple CSV file
        df = pd.DataFrame({
            'Address': addresses,
            'Audit_Date': datetime.now().strftime("%Y-%m-%d"),
            'Risk_Level': 'Pending Review'
        })
        
        df.to_csv('database.csv', index=False)
        print(f"Scraped {len(addresses)} properties successfully.")
        browser.close()

if __name__ == "__main__":
    run_scraper()
