import pandas as pd
import time as t
start = t.time()

basics = pd.read_table("title.basics.tsv")
ratings = pd.read_table("title.ratings.tsv")
basics.to_csv("title.basics.csv")
ratings.to_csv("title.ratings.csv")

print("it takes %ss" % (t.time() - start))
