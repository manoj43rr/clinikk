import pandas as pd
import streamlit as st

st.header("Renewal Distributor")

n = st.number_input("Enter the number of person into renewals : ")

inputFile = st.file_uploader("Upload the File", type=["xlsx", "xls"])

if inputFile is not None:
    data = pd.read_excel(inputFile, engine="openpyxl")

    st.dataframe(data)
