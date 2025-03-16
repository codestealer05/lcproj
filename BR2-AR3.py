import pandas as pd
import plotly.express as px
from flask import Flask, render_template, request, redirect
import json

# Load the dataset
df = pd.read_csv("cleanData.csv")

# Calculate the mean of the average ratings
mean = df.loc[:, "averageRating"].mean()
# print(mean)

# Calculate the mean of the average ratings (method by hand)
mean = sum(df["averageRating"]) / len(df["averageRating"])
print(f"This is the average rating of all movies: {mean}")

# Calculate the median of the start years
median = df.loc[:, "startYear"].median()
# print(median)

# Calculate the median of the start years (method by hand)
sortedYears = sorted(df["startYear"])
if len(df["startYear"]) % 2 == 0:
    median = (sortedYears[len(sortedYears) // 2 - 1] + sortedYears[len(sortedYears) // 2]) / 2
    print(f"This is the median of years: {median}")
else:
    median = sortedYears[len(sortedYears) // 2]
    print(f"This is the median of years: {median}")

# Calculate the mode of the genres
mode = df.loc[:, "genres"].mode()
# print(mode)

# Create a list of genres
genres = list(df["genres"])

# Split genres and create a new list
genresnew = []
for genre in genres:
    temp = genre.split(",")
    for j in temp:
        genresnew.append(j)
# print(genresnew)

# Create a set of unique genres
genresset = {"Action"}
for genre in genres:
    temp = genre.split(",")
    for j in temp:
        genresset.add(j)
genresset = sorted(genresset)
# print(genresset)

# Calculate the mode of the list of genres
mode = ""
temp = 0
for genre in genresset:
    temp2 = genresnew.count(genre)
    if temp2 > temp:
        temp = temp2
        mode = genre
print(f"This is the mode of the list of genres: {mode}")

# print(sorted(genresset))

# Define the popular1 function to calculate average ratings for each genre
def popular1():
    rating = {}
    for genre in genresset:
        filmCount = 0
        ratingSum = 0
        for i in range(len(df)):
            film = df.iloc[i]
            if genre in film["genres"]:
                filmCount += 1
                ratingSum += film["numVotes"]
        if filmCount > 0:
            rating[genre] = round(ratingSum / filmCount, 3)
    return rating

# Define the popular2 function to calculate average ratings for each genre pair
def popular2():
    rating = {}
    for genre1 in genresset:
        for genre2 in genresset:
            if genre2 == genre1:
                break
            # Filter rows where both genres are present
            filtered_df = df[df["genres"].str.contains(genre1, na=False)]
            filtered_df = filtered_df[filtered_df["genres"].str.contains(genre2, na=False)]
            filmCount = len(filtered_df)
            if filmCount > 0:
                ratingSum = filtered_df["numVotes"].sum()
                rating[genre1 + " " + genre2] = round(ratingSum / filmCount, 3)
    return rating

# Initialize global variables for HTML content
historyHeroHTML = ""
heroHTML = ""
formDisabledHTML = ""
movieRecommendationHTML = ""

# Initialize the Flask application
app = Flask(__name__)

# Define the home route
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

# Define the scatterchart route to display a scatter plot
@app.route("/scatterchart")
def scatterchart():
    scatterchart = px.scatter(x=df["averageRating"], y=df["numVotes"],
                              title="Chart showing the relationship between average rating and the number of Votes of a movie")
    scatterchart.update_layout(
        xaxis_title="Average Rating",
        yaxis_title="Number of Votes"
    )
    
    # Add a horizontal line at the average rating
    scatterchart.add_shape(
        type="line",
        x0=6.5955,
        y0=0,
        x1=6.5955,
        y1=df["numVotes"].max(),
        line=dict(color="Green", width=2, dash="dash"),
    )
    
    scatterchart_html = scatterchart.to_html(full_html=False)
    return render_template("scatterchart.html", scatterchart=scatterchart_html)

# @app.route("/piechartold")
# def piechartold():
#     dfpc = df[["primaryTitle", "numVotes"]]
#     dfpc = dfpc.head(10)
#     piechartold = px.pie(dfpc, values="numVotes", names="primaryTitle", title="Number of votes of first "
#     "10 movies in the list")
#     piechartold_html = piechartold.to_html(full_html=False)
#     return render_template("piechartold.html", piechartold=piechartold_html)

# Define the piechart route to display a pie chart of genre popularity
@app.route("/piechart")
def piechart():
    genrecount = []
    for genre in genresset:
        genrecount.append(genresnew.count(genre))
    dfpc2 = pd.DataFrame({"genres": list(genresset), "count": genrecount})
    piechart = px.pie(dfpc2, values="count", names="genres", title="Popularity of Genres")
    piechart_html = piechart.to_html(full_html=False)
    return render_template("piechart.html", piechart=piechart_html)

# Define the form route to handle form submissions
@app.route("/form", methods=["GET", "POST"])
async def form():
    global historyHeroHTML
    global heroHTML
    global formDisabledHTML
    global movieRecommendationHTML
    if request.method == "POST":
        formData = request.get_json()
        selectedGenres = formData.get("genres")
        selectedDecade = formData.get("decade")
        agreement = formData.get("agreement")

        dataDict = {
            "genres": selectedGenres,
            "decade": selectedDecade,
            "agreement": agreement
        }

        try:
            with open("data", "r") as file:
                data = json.load(file)  # Read existing data
        except FileNotFoundError:
            data = []

        data.append(dataDict)
        with open("data", "w") as file:
            json.dump(data, file, indent=4)

        historyHeroHTML = f"""
    <section class="hero is-medium is-success">
        <div class="hero-body">
            <p class="title">According to users of this service: </p>
            <div class="is-size-5">
                Three most popular movie genres are: <b>{await find3Genres()}</b> <br />
                The "golden decade" of cinematography is <b>{await findDecade()}</b> <br />
                Whether a "good movie" should be longer than 2 hours is <b>{await findOpinion()}</b>
            </div>
        </div>
    </section>
    """

        heroHTML = f"""
            <section class="hero is-small is-success">
            <div class="hero-body">
    <p class="title">Your submission:</p>
        <div class="columns">
            <div class="column">
                <div class="is-size-5">{selectedGenres}</div>
            </div>
            <div class="column">
                <div class="is-size-5">{selectedDecade}</div>
            </div>
            <div class="column">
                <div class="is-size-5">{agreement}</div>
            </div>
        </div>
    </div>
    </section>
            """

        formDisabledHTML = "disabled"

        # Checking the type of the variables to make sure they are different for AR2
        # print(type(selectedGenres), type(selectedDecade), type(agreement))
        # the output is <class 'list'> <class 'int'> <class 'bool'>
        
        movieRecommendationHTML = f"""
        <section class="hero is-medium is-success">
          <div class="hero-body">
            <p class="title">Based on your preferences these movies were found in the database</p>
            <p class="is-size-5">{findMovies(selectedGenres, selectedDecade, agreement)}</p>
          </div>
        </section>
        """
        return redirect("/form")

        # Handle GET requests (e.g., render a form)
    return render_template("form.html", formDisabled=formDisabledHTML, historyHero=historyHeroHTML, newHero=heroHTML, movieRecommendation=movieRecommendationHTML)

# Define the recommendation route to display top genres and genre pairs
@app.route("/recommendation")
def recommendation():
    global top13
    global top23
    return render_template("recommendation.html", top1=top13, top2=top23)

# Define the find3Genres function to find the top 3 genres
async def find3Genres():
    chosenGenres = []
    popularGenres = []
    with open("data", "r") as f:
        data = json.load(f)
        for entry in data:
            for genre in entry["genres"]:
                chosenGenres.append(genre)
    chosenGenresDF = pd.Series(chosenGenres)
    for i in range(3):
        temp = chosenGenresDF.mode()[0]
        popularGenres.append(temp)
        chosenGenresDF = chosenGenresDF[(chosenGenresDF != temp)]
    return f"{popularGenres[0]}, {popularGenres[1]}, {popularGenres[2]}"

# Define the findDecade function to find the most popular decade
async def findDecade():
    chosenDecades = []
    with open("data", "r") as f:
        data = json.load(f)
        for entry in data:
            chosenDecades.append(entry["decade"])

    chosenDecadesDF = pd.Series(chosenDecades)
    temp = chosenDecadesDF.mode()[0]
    return temp

# Define the findOpinion function to find the most common opinion on movie length
async def findOpinion():
    chosenOpinion = []
    with open("data", "r") as f:
        data = json.load(f)
        for entry in data:
            chosenOpinion.append(entry["agreement"])

    chosenOpinionDF = pd.Series(chosenOpinion)
    temp = chosenOpinionDF.mode()[0]
    return temp

# Define the findMovies function to find movies based on user preferences
def findMovies(genres, decade, opinion):
    selectedDF = df[df["startYear"].between(decade, decade + 9)]
    selectedDF.loc[:, "runtimeMinutes"] = pd.to_numeric(selectedDF["runtimeMinutes"], errors="coerce")
    if opinion:
        selectedDF = selectedDF[selectedDF["runtimeMinutes"] > 120]
    else:
        selectedDF = selectedDF[selectedDF["runtimeMinutes"] <= 120]
    # print(selectedDF)
    rowsToAdd = []
    for i in range(len(selectedDF)):
        temp = 0
        for genre in genres:
            if genre in selectedDF.iloc[i, 7]:  # 7 corresponds to genres
                temp += 1
        rowsToAdd.append({"tconst": selectedDF.iloc[i, 0], "genreCount": temp})
    refinedDF = pd.DataFrame(rowsToAdd)

    selectedDF = pd.merge(selectedDF, refinedDF, on="tconst")

    selectedDF = selectedDF.sort_values(by=["genreCount", "averageRating"], ascending=[False, False]).head(5)

    suggestion = ""
    for i in range(len(selectedDF)):
        suggestion += selectedDF.iloc[i, 3]
        suggestion += ", "
        suggestion += str(selectedDF.iloc[i, 5])
        suggestion += "<br />"

    return suggestion

# print(findMovies(["Action", "Adventure", "Family"], 2000, True))

# Calculate the top 3 genres
myRating = popular1()
# Check the output of the dictionary
# for genre in genresset:
#     print(f"{genre}: {myRating[genre]}")
top1 = max(myRating, key=myRating.get)
myRating.pop(top1)
top2 = max(myRating, key=myRating.get)
myRating.pop(top2)
top3 = max(myRating, key=myRating.get)
top13 = f"Top 3 genres: {top1}, {top2}, {top3}"

# Calculate the top 3 genre pairs
myRating2 = popular2()
# Check the output of the dictionary
# for genre1 in genresset:
#     for genre2 in genresset:
#         if genre1 == genre2:
#             break
#         try:
#             print(f"{genre1} {genre2}: {myRating2[genre1 + " " + genre2]}")
#         except KeyError:
#             print(f"{genre1} {genre2}: N/A")
top1_2 = max(myRating2, key=myRating2.get)
myRating2.pop(top1_2)
top2_2 = max(myRating2, key=myRating2.get)
myRating2.pop(top2_2)
top3_2 = max(myRating2, key=myRating2.get)
top23 = f"Top 3 genre pairs: {top1_2}, {top2_2}, {top3_2}"

# Run the Flask application
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=6006, debug=False)

