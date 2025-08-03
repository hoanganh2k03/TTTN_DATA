# components/data_loader.py
import pandas as pd

def load_data():
    df = pd.read_csv("sales_data_sample_clean.csv", encoding='latin1')
    df["ORDERDATE"] = pd.to_datetime(df["ORDERDATE"])
    df["MONTH"] = df["ORDERDATE"].dt.to_period("M").astype(str)
    return df
