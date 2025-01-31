import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_excel("data.xlsx", engine="openpyxl")
data = data.dropna(subset="Clinikk ID")
data2 = pd.read_excel("data2.xlsx", engine="openpyxl")
data2 = data2.dropna(subset="Clinikk ID")



data['Month'] = data['Sale Date'].dt.strftime('%b')  # 'Jan', 'Feb', 'Mar', etc.
data['Year'] = data['Sale Date'].dt.year


requiredColumns = ['Sale Date', 'Agent Name', 'Full Name','Phone', 'Clinikk ID', 'Type', 'Coverage',
       'Payment Plan', 'Price', 'Plan', 'GHI Status','Date GHI Processed','Month', 'Year']

newData = data[requiredColumns]
newData = pd.DataFrame(newData)

newData = newData.dropna(subset="Sale Date")

newData = newData.convert_dtypes()


Months = newData["Month"].unique()
years = newData["Year"].unique()

# Streamlit title
st.title("B2C OnBoarding Live Dashboard")

# User selects the year and month
selectedYear = st.selectbox("Select Year:", years)
selectedMonth = st.selectbox("Select Month:", Months)

filteredData = newData[(newData["Month"] == selectedMonth) & (newData["Year"] == selectedYear)]

sentCases = filteredData[filteredData["GHI Status"] == "Sent"]
pendingCases = filteredData[filteredData["GHI Status"] == "Pending"]
processingCases = filteredData[filteredData["GHI Status"].isna()]

st.write(f"there are a total of {len(sentCases)} GHI Status is 'sent'")
st.write(f"there are a total of {len(pendingCases)} GHI Status is 'pending")
st.write(f"there are a total of {len(processingCases)} GHI Status is 'NA'")

filteredIds = sentCases["Clinikk ID"].unique()

sentData = data2[data2["Clinikk ID"].isin(filteredIds)]

newRequiredColumn = ["COI Uploaded Date","Clinikk ID"]
sentData = sentData[newRequiredColumn]

sentData = sentCases.merge(sentData[["COI Uploaded Date", "Clinikk ID"]], on = "Clinikk ID")
sentMissingCases = sentData[sentData["COI Uploaded Date"].isna()]
sentData = sentData.dropna(subset="COI Uploaded Date")

st.write("Data of people whose GHI status is marked 'Sent' and COI uploaded date was fetched")
st.dataframe(sentData)

st.write("Data of people whose GHI status is marked 'Sent' and COI uploaded date couldn't be fetched")
st.dataframe(sentMissingCases)

mythicalPendingFilteredIds = pendingCases["Clinikk ID"].unique()

if(len(mythicalPendingFilteredIds)):
    mythicalPendingData = data2[data2["Clinikk ID"].isin(mythicalPendingFilteredIds)]

    newRequiredColumn = ["COI Uploaded Date","Clinikk ID"]
    mythicalPendingData = mythicalPendingData[newRequiredColumn]

    mythicalPendingData = pendingCases.merge(mythicalPendingData[["COI Uploaded Date", "Clinikk ID"]], on = "Clinikk ID")

actualPendingCases = pendingCases[~pendingCases["Clinikk ID"].isin(mythicalPendingData["Clinikk ID"].unique())]
st.dataframe(actualPendingCases)

unUsualIds = processingCases["Clinikk ID"].unique()
if(len(unUsualIds)):
    unUsualData = data2[data2["Clinikk ID"].isin(unUsualIds)]

    newRequiredColumn = ["COI Uploaded Date","Clinikk ID"]
    unUsualData = unUsualData[newRequiredColumn]
    mythicalPendingData = pd.concat([mythicalPendingData,unUsualData], ignore_index=True)
    st.write("Data of people whose GHI status is marked 'Pending' and COI uploaded date was fetched")
    st.dataframe(mythicalPendingData)

st.write("Data of people whose GHI status is marked 'NA' and COI uploaded date was not fetched")
st.dataframe(processingCases)

y = np.array([len(sentData), len(mythicalPendingData), len(actualPendingCases),len(processingCases)])
mylabels = ["Data with COI date", "data with GHI status 'pending' but COI date found", "actual Pending cases", "Maybe processing cases with 'Na' GHI status"]

fig, ax = plt.subplots()
ax.pie(y, labels=mylabels, autopct='%1.1f%%')  # Adding percentage labels

# Display the chart in Streamlit
st.pyplot(fig)
