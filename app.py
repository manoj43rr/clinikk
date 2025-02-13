import pandas as pd
import streamlit as st

st.header("Renewal Distributor")

n = st.number_input("Enter the number of person into renewals : ")

inputFile = st.file_uploader("Upload the File", type=["xlsx", "xls", "csv"])

if inputFile is not None:
    data = pd.read_excel(inputFile, engine="openpyxl")

    priceLi = data[data.columns[1]].tolist()
    st.caption(f"Length : {len(priceLi)}")

