import pandas as pd
import streamlit as st

# Read data from Excel
data = pd.read_excel("data.xlsx", engine="openpyxl")

# Extract month and year from 'Sale Date'
data['Month'] = data['Sale Date'].dt.strftime('%b')
data['Year'] = data['Sale Date'].dt.year

# Columns to keep
requiredColumns = ['Sale Date', 'Agent Name', 'Full Name', 'Phone', 'Clinikk ID', 'Type', 'Coverage', 'Payment Plan', 'Price', 'Plan', 'GHI Status', 'Date GHI Processed', 'Month', 'Year']
newData = data[requiredColumns]

# Drop rows where 'Sale Date' is missing
newData = newData.dropna(subset=["Sale Date"])

# Convert data types
newData = newData.convert_dtypes()

# Extract unique months and years for the selectbox options
Months = newData["Month"].unique()
years = newData["Year"].unique()

# Streamlit title
st.title("B2C OnBoarding Live Dashboard")

# User selects the year and month
selectedYear = st.selectbox("Select Year:", years)
selectedMonth = st.selectbox("Select Month:", Months)

# Filter data based on the selected year and month
filteredData = newData[(newData["Month"] == selectedMonth) & (newData["Year"] == selectedYear)]

# Display filtered data
st.subheader(f"Data for {selectedMonth} and {selectedYear}")
st.dataframe(filteredData)
