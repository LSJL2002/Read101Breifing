import streamlit as st
import pandas as pd

st.set_page_config(page_title="Children Session Tracker", layout="wide")

st.title("🎒 Kids Session Filter App")
st.write("Upload your `export-children.xlsx` file below to instantly filter for children with 5 sessions or less remaining (excluding those without registered total sessions).")

uploaded_file = st.file_uploader("Choose your Excel file (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Load the Excel file skipping the metadata rows
        df = pd.read_excel(uploaded_file, skiprows=3)
        
        # Set the first row (index 0) as the header
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)
        
        # Clean the 'Remaining' and 'Total' columns and convert to numeric values
        df['Remaining'] = pd.to_numeric(df['Remaining'].replace('-', 0), errors='coerce').fillna(0)
        df['Total'] = pd.to_numeric(df['Total'].replace('-', 0), errors='coerce').fillna(0)

        df['Duration_days'] = df['Duration'].astype(str).str.extract(r'(\d+)').astype(float).fillna(0)

        # Filter for kids with 5 sessions or less remaining, but ensuring they have a valid 'Total' session count > 0
        kids_filtered = df[(df['Duration_days'] <= 14) & (df['Total'] > 0)]
        
        # Keep relevant columns for clear presentation
        columns_to_show = ['Name', 'English Name', 'School', 'Grade', 'Total', 'Used', 'Remaining', 'Duration', 'Status']
        filtered_df = kids_filtered[columns_to_show]
        
        st.success(f"Successfully found {len(filtered_df)} kids matching the criteria!")
        
        # Display the filtered DataFrame
        st.dataframe(filtered_df, use_container_width=True)
        
        # Download Button for the filtered results
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered List as CSV",
            data=csv,
            file_name="filtered_kids_14_days_or_less.csv",
            mime="text/csv",
        )
        
    except Exception as e:
        st.error(f"An error occurred while parsing the file: {e}")
else:
    st.info("Please upload an Excel file to get started.")
