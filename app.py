import pandas as pd
import streamlit as st

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    processed_data = output.getvalue()
    return processed_data

def GreedyFriendsAlgorithm(prices, k):
    n = len(priceLi)

    if k > n:
        print("can't assign",{n},"tasks to",{k},"individuals.")
        return None
    
    prices.sort(reverse = True)
    friendsTotal = [0] * k
    friendsAssignments = [[] for i in range(k)]

    for price in prices:
        lowestTotalFriend = friendsTotal.index(min(friendsTotal))
        friendsTotal[lowestTotalFriend] += price
        friendsAssignments[lowestTotalFriend].append(price)

    return friendsAssignments
        
def AssigningClinikkIds(row):
    amt =  row["AssignedAmount"]
    data1 = data[(data["Product Price New"] == amt) & ~(data["Clinikk ID"].isin(usedIds))]
    usedIds.append(data1["Clinikk ID"].iloc[0])
    return data1["Clinikk ID"].iloc[0]
    

st.header("Renewal Distributor")

n = st.number_input("Enter the number of person into renewals : ")

persons = []

usedIds = []

if n > 0:    
    for i in range(1, n):
        temp = 'Person' + i
        persons.append(temp)

inputFile = st.file_uploader("Upload the File", type=["xlsx", "xls", "csv"])

if inputFile is not None:
    data = pd.read_excel(inputFile, engine="openpyxl")
    
    priceLi = data[data.columns[1]].tolist()
    
    Assignments = GreedyFriendsAlgorithm(priceLi, len(persons))
    
    for i in range(0, len(persons)):
        print("Works assigned to person ",{i}," is ",{len(Assignments[i])}," and Total of ",{sum(Assignments[i])})
    
    dataFrames = [None] * len(persons)
    
    for i in range(0, len(persons)):
        dataFrames[i] = pd.DataFrame(Assignments[i], columns=["AssignedAmount"])
        dataFrames[i]["Clinikk Id"] = 0
        dataFrames[i]["Person"] = persons[i]
    
    for i in range(0, len(persons)):
        dataFrames[i]["Clinikk Id"] = dataFrames[i].apply(AssigningClinikkIds, axis = 1)
    
    resultDf = pd.DataFrame()
    
    for i in range(0, len(persons)):
        resultDf = pd.concat([resultDf, dataFrames[i]], axis=0)

excel_data = to_excel(resultDf)

st.download_button(
    label="Download data as Excel",
    data=excel_data,
    file_name="Output.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


    

