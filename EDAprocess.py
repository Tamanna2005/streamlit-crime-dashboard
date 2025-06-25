import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
df=pd.read_csv(r"c:\Users\hp\Downloads\pythonDashboardDataset.csv")
df.columns=df.columns.str.strip().str.upper()
df["REPORTEDDATE"]=pd.to_datetime(df["REPORTEDDATE"],errors="coerce")
df["REPORTEDTIME"]=pd.to_datetime(df["REPORTEDTIME"],errors="coerce")
df["REPORTEDDATE"]=df["REPORTEDDATE"].dt.tz_localize(None)
print("Data loaded successfully\n")
print("First 5 rows: \n",df.head())
print("Last 5 rows: \n",df.tail())
print("DataFrame info: \n")
df.info()
print("Summary Statastics: \n",df.describe())
print("Missing Values: \n",df.isnull().sum())
df.dropna(subset=["REPORT_NUMBER"],inplace=True)
offence_cols=["NIBRS_CODED_OFFENSE","NIBRS_OFFENSE_CODE","NIBRS_OFFENSE_CATEGORY",
              "NIBRS_OFFENSE_TYPE","NIBRS_CRIME_AGAINST","NIBRS_OFFENSE_GROUPING"]
df[offence_cols]=df[offence_cols].fillna("Unknown")
df["VIOLATION"].fillna("Not Provided",inplace=True)
df["XCOORD"].fillna(df["XCOORD"].mean(),inplace=True)
df["YCOORD"].fillna(df["YCOORD"].mean(),inplace=True)
df.drop("TRACT",axis=1,inplace=True)
df["NEIGHBORHOOD"].fillna("Unknown",inplace=True)
df["BLOCK_ADDRESS"].fillna("Unknown",inplace=True)
df.to_csv("cleaned_crime_data.csv",index=False)