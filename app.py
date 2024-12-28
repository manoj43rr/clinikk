import streamlit as st
import pandas as pd

# Load the dataset
data = pd.read_csv("data.csv")

# Create DataFrame from the dataset
df = pd.DataFrame(data)

# Title of the dashboard
st.title("Business Data Dashboard")

# Dropdown menu for selecting the business
businessDropMenu = df["Business"].unique()
selected_business = st.selectbox("Select Business Name:", businessDropMenu)

# Filter the dataframe based on the selected business
filtered_df = df[df["Business"] == selected_business]

# Display the filtered data
st.subheader(f"Data for {selected_business}")
st.dataframe(filtered_df)
