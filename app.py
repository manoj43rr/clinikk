import streamlit as st
import pandas as pd
import numpy as np

# Load the dataset
database = pd.read_csv("update.csv")

# Create DataFrame from the dataset
PreviousDf = pd.DataFrame(database)

# Title of the dashboard
st.title("Business Data Dashboard")

# Dropdown menu for selecting the business
businessDropMenu = PreviousDf["Sale_center"].unique()
selected_business = st.selectbox("Select Business Name:", businessDropMenu)

# Filter the dataframe based on the selected business
filteredBusinessDf = PreviousDf[PreviousDf["Sale_center"] == selected_business]

# Display the filtered data
st.subheader(f"Data for {selected_business}")
st.dataframe(filteredBusinessDf)

# File uploader
file = st.file_uploader("Insert the New Data to be compared with the previous month data", type=["csv"])

if file is not None:
    try:
        # Read the uploaded file
        newData = pd.read_csv(file)
        
        # Display the uploaded data
        st.dataframe(newData)
        
        # Select a column to compare
        ColumnMenu = newData.columns.tolist()
        selected_Column = st.selectbox("Select the Column to Compare:", ColumnMenu)
        
        # Display the selected column
        newPhoneNumbers = newData[selected_Column]
    
        st.write(f"Data from column: {selected_Column}")
        st.dataframe(newPhoneNumbers)

        oldPhoneNumbers = filteredBusinessDf["RMN"]

        renewalPhoneNumbers = list(set(newPhoneNumbers) & set(oldPhoneNumbers))
        missingPhoneNumbers = list(set(newPhoneNumbers) - set(renewalPhoneNumbers))
        deletionPhoneNumbers = list(set(missingPhoneNumbers))
        additionPhoneNumbers = list(set(oldPhoneNumbers) - set(newPhoneNumbers))

        st.write("Total Renewal Members count: ", {len(renewalPhoneNumbers)})
        st.write("Total Members who are new: ",{len(additionPhoneNumbers)})
        st.write("Total Members ending their insurance: ",{len(deletionPhoneNumbers)})

        renewalMembers = filteredBusinessDf[filteredBusinessDf["RMN"].isin(renewalPhoneNumbers)]
        deletionMembers = newData[newData[selected_Column].isin(deletionPhoneNumbers)]
        newMembers = filteredBusinessDf[filteredBusinessDf["RMN"].isin(additionPhoneNumbers)]

        st.write("Renewal Members are:")
        st.dataframe(renewalMembers)

        st.write("Members to be Deleted:")
        st.dataframe(deletionMembers)

        st.write("New Members to be added:")
        st.dataframe(newMembers)

    except Exception as e:
        # Handle errors gracefully
        st.error(f"Error reading the file: {e}")
else:
    st.info("Please upload a CSV file to proceed.")
