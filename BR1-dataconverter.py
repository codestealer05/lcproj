import pandas as pd
# import time as t
# start = t.time()

# Preclean the data
basics = pd.read_table("title.basics.tsv")
ratings = pd.read_table("title.ratings.tsv")
basics.to_csv("title.basics.csv")
ratings.to_csv("title.ratings.csv")

# print("it takes %ss" % (t.time() - start))

# The data has already been cleaned, so we can skip the cleaning process
# Please run BR2-AR3.py 