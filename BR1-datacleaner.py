import pandas as pd
# import time as t
# start = t.time()

# Cleaning the data
# Read the data
basics = pd.read_csv("title.basics.csv")
ratings = pd.read_csv("title.ratings.csv")

# Remove all rows which are not movies
onlyMovies = basics[basics["titleType"] == "movie"]
#onlyMovies.to_csv("dfclean.csv")

# Remove all rows with genres = \N
onlyGenres = onlyMovies[onlyMovies["genres"] != r"\N"]
#onlyGenres.to_csv("onlyGenres.csv")

# Remove all rows where ratings are less than 10000
minVotes = ratings[ratings["numVotes"] > 9999]
#print(minVotes)
#minVotes.to_csv("minVotes100.csv")

# Merge the data files
cleanData = pd.merge(onlyGenres, minVotes, on="tconst")
cleanData = cleanData[["tconst", "titleType", "primaryTitle", "originalTitle", "isAdult", "startYear", "runtimeMinutes", "genres", "averageRating", "numVotes"]]
print(cleanData)
cleanData.to_csv("cleanData.csv", index=False)

# print("it takes %ss" % (t.time() - start))

# The data has already been cleaned, so we can skip the cleaning process
# Please run BR2-AR3.py 