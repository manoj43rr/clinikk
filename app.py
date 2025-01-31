import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Load Data
data = pd.read_excel("data.xlsx", engine="openpyxl").dropna(subset=["Clinikk ID"])
data2 = pd.read_excel("data2.xlsx", engine="openpyxl").dropna(subset=["Clinikk ID"])

# Ensure 'Sale Date' is in datetime format
data['Sale Date'] = pd.to_datetime(data['Sale Date'], errors='coerce')
data = data.dropna(subset=['Sale Date'])

# Extract Month & Year
data['Month'] = data['Sale Date'].dt.strftime('%b')  # 'Jan', 'Feb', 'Mar', etc.
data['Year'] = data['Sale Date'].dt.year

# Required Columns
requiredColumns = ['Sale Date', 'Agent Name', 'Full Name','Phone', 'Clinikk ID', 'Type', 'Coverage',
                   'Payment Plan', 'Price', 'Plan', 'GHI Status','Date GHI Processed','Month', 'Year']
newData = data[requiredColumns].convert_dtypes()

# Streamlit UI
st.title("B2C OnBoarding Live Dashboard")

# Dropdowns for selection
selectedYear = st.selectbox("Select Year:", sorted(newData["Year"].unique()))
selectedMonth = st.selectbox("Select Month:", sorted(newData["Month"].unique()))

# Filter Data
filteredData = newData[(newData["Month"] == selectedMonth) & (newData["Year"] == selectedYear)]

# Categorize Cases
sentCases = filteredData[filteredData["GHI Status"] == "Sent"]
pendingCases = filteredData[filteredData["GHI Status"] == "Pending"]
processingCases = filteredData[filteredData["GHI Status"].isna()]

# Display Counts
st.write(f"There are a total of {len(sentCases)} GHI Status is 'sent'")
st.write(f"There are a total of {len(pendingCases)} GHI Status is 'pending'")
st.write(f"There are a total of {len(processingCases)} GHI Status is 'NA'")

# Fetch Sent Data
filteredIds = sentCases["Clinikk ID"].unique()
sentData = data2[data2["Clinikk ID"].isin(filteredIds)][["COI Uploaded Date", "Clinikk ID"]]
if not sentData.empty:
    sentData = sentCases.merge(sentData, on="Clinikk ID", how="left")

sentMissingCases = sentData[sentData["COI Uploaded Date"].isna()]
sentData = sentData.dropna(subset=["COI Uploaded Date"])

# Display Sent Data
st.write("Data of people whose GHI status is marked 'Sent' and COI uploaded date was fetched")
st.dataframe(sentData)

st.write("Data of people whose GHI status is marked 'Sent' and COI uploaded date couldn't be fetched")
st.dataframe(sentMissingCases)

# Fetch Pending Data
mythicalPendingData = pd.DataFrame()
mythicalPendingFilteredIds = pendingCases["Clinikk ID"].unique()
if len(mythicalPendingFilteredIds):
    mythicalPendingData = data2[data2["Clinikk ID"].isin(mythicalPendingFilteredIds)][["COI Uploaded Date", "Clinikk ID"]]
    mythicalPendingData = pendingCases.merge(mythicalPendingData, on="Clinikk ID", how="left")

actualPendingCases = pendingCases[~pendingCases["Clinikk ID"].isin(mythicalPendingData["Clinikk ID"].unique())]
st.dataframe(actualPendingCases)

# Fetch Processing Data
unUsualData = pd.DataFrame()
unUsualIds = processingCases["Clinikk ID"].unique()
if len(unUsualIds):
    unUsualData = data2[data2["Clinikk ID"].isin(unUsualIds)][["COI Uploaded Date", "Clinikk ID"]]
    mythicalPendingData = pd.concat([mythicalPendingData, unUsualData], ignore_index=True)

st.write("Data of people whose GHI status is marked 'NA' and COI uploaded date was not fetched")
st.dataframe(processingCases)

# Pie Chart
y = np.array([
    len(sentData) if not sentData.empty else 0,
    len(mythicalPendingData) if not mythicalPendingData.empty else 0,
    len(actualPendingCases) if not actualPendingCases.empty else 0,
    len(processingCases) if not processingCases.empty else 0
])
labels = ["Data with COI date", "Pending cases with COI date", "Actual Pending", "NA GHI status cases"]

fig, ax = plt.subplots()
ax.pie(y, autopct='%1.1f%%')
ax.legend(labels, title="Case Categories", loc="best")
st.pyplot(fig)
