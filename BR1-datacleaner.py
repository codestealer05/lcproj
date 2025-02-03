import pandas as pd
import time as t
start = t.time()

basics = pd.read_csv("title.basics.csv")
ratings = pd.read_csv("title.ratings.csv")

onlyMovies = basics[basics["titleType"] == "movie"]
#onlyMovies.to_csv("dfclean.csv")

onlyGenres = onlyMovies[onlyMovies["genres"] != r"\N"]
#onlyGenres.to_csv("onlyGenres.csv")

minVotes = ratings[ratings["numVotes"] > 9999]
#print(minVotes)
#minVotes.to_csv("minVotes100.csv")

cleanData = pd.merge(onlyGenres, minVotes, on="tconst")
cleanData = cleanData[["tconst", "titleType", "primaryTitle", "originalTitle", "isAdult", "startYear", "runtimeMinutes", "genres", "averageRating", "numVotes"]]
print(cleanData)
cleanData.to_csv("cleanData.csv", index=False)

print("it takes %ss" % (t.time() - start))
