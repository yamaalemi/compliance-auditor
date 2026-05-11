import streamlit as st
import pandas as pd

st.set_page_config(page_title="Compliance Auditor", page_icon="🛡️")

st.title("🛡️ 2026 Landlord Compliance Portal")
st.write("Check if your rental property meets the new May 2026 standards.")

# Load the data we scraped
try:
    df = pd.read_csv('database.csv')
    
    search = st.text_input("Enter your property postcode:").upper()
    
    if search:
        # Check if the postcode is in our audit list
        results = df[df['Address'].str.contains(search)]
        if not results.empty:
            st.error(f"⚠️ Warning: We have flagged {len(results)} properties in this area.")
            st.dataframe(results)
            st.button("Request Full Risk Report")
        else:
            st.success("✅ No immediate legal risks found in our latest audit.")
except:
    st.info("The auditor is currently scanning local agents. Please refresh in 5 minutes.")
