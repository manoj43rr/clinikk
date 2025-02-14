import streamlit as st
import pandas as pd
from io import BytesIO

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    processed_data = output.getvalue()
    return processed_data

def GreedyFriendsAlgorithm(prices, k):
    n = len(prices)
    if k > n:
        st.error(f"Can't assign {n} tasks to {k} individuals.")
        return None
    
    prices.sort(reverse=True)
    friendsTotal = [0] * k
    friendsAssignments = [[] for _ in range(k)]

    for price in prices:
        lowestTotalFriend = friendsTotal.index(min(friendsTotal))
        friendsTotal[lowestTotalFriend] += price
        friendsAssignments[lowestTotalFriend].append(price)

    return friendsAssignments

def AssigningClinikkIds(row):
    amt = row["AssignedAmount"]
    data1 = data[(data[data.columns[1]] == amt) & ~(data[data.columns[0]].isin(usedIds))]

    if not data1.empty:
        usedIds.append(data1["Clinikk ID"].iloc[0])
        return data1["Clinikk ID"].iloc[0]
    else:
        return None

st.header("Renewal Distributor")

# Ensure minimum value is 1
n = st.number_input("Enter the number of persons into renewals:", min_value=1, step=1)

# Define persons inside the if condition
persons = []
usedIds = []

st.caption('📌 The first column name must be "Clinikk ID"')

if n > 0:    
    for i in range(n):  # Start from 0
        temp = f'Person{i+1}'  # Corrected string formatting
        persons.append(temp)

inputFile = st.file_uploader("Upload the File", type=["xlsx", "xls", "csv"])

if inputFile is not None:
    if inputFile.name.endswith(".csv"):
        data = pd.read_csv(inputFile)
    else:
        data = pd.read_excel(inputFile, engine="openpyxl")
    
    priceLi = data[data.columns[1]].tolist()
    
    Assignments = GreedyFriendsAlgorithm(priceLi, len(persons))
    
    if Assignments is not None:
        for i in range(len(persons)):
            st.write(f"Works assigned to {persons[i]}: {len(Assignments[i])} tasks, Total: {sum(Assignments[i])}")

        dataFrames = []
        
        for i in range(len(persons)):
            df = pd.DataFrame(Assignments[i], columns=["AssignedAmount"])
            df["Clinikk Id"] = 0
            df["Person"] = persons[i]
            dataFrames.append(df)

        for i in range(len(persons)):
            dataFrames[i]["Clinikk Id"] = dataFrames[i].apply(AssigningClinikkIds, axis=1)
        
        resultDf = pd.concat(dataFrames, axis=0)
        
        excel_data = to_excel(resultDf)
        
        st.download_button(
            label="Download data as Excel",
            data=excel_data,
            file_name="Output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
