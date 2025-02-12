import pandas as pd

df = pd.read_csv("cleanData.csv")
print(df["startYear"].max())
