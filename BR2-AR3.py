import pandas as pd
import plotly.express as px
from flask import Flask, render_template, request, jsonify, redirect, url_for
from markupsafe import escape
import json

df = pd.read_csv("cleanData.csv")
mean = df.loc[:, "averageRating"].mean()
print(mean)

mean = sum(df["averageRating"])/len(df["averageRating"])
print(mean)

median = df.loc[:, "startYear"].median()
print(median)

sortedYears = sorted(df["startYear"])
if len(df["startYear"])%2 == 0:
    median = (sortedYears[len(sortedYears)//2 - 1] + sortedYears[(len(sortedYears)//2)])/2
    print(median)
else:
    median = sortedYears[len(sortedYears)//2]
    print(median)


mode = df.loc[:, "genres"].mode()
print(mode)

genres = list(df["genres"])

genresnew = []
for genre in genres:
    temp = genre.split(",")
    for j in temp:
        genresnew.append(j)
#print(genresnew)
        
genresset = {"Action"}
for genre in genres:
    temp = genre.split(",")
    for j in temp:
        genresset.add(j)     
#print(sorted(genresset))

mode = ""
temp = 0
for genre in genresset:
    temp2 = genresnew.count(genre)
    if  temp2 > temp:
        temp = temp2
        mode = genre

print(mode)

#print(sorted(genresset))

historyHeroHTML = ""
heroHTML = ""
formDisabledHTML = ""
movieRecommendationHTML = ""

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def work():
    return render_template("home.html")

@app.route("/hello/<username>")
def hello(username):
    username = input("Enter username: ")
    return (f"hello {escape(username)}", username)

@app.route("/scatterchart")
def scatterchart():
    scatterchart = px.scatter(x=df["averageRating"], y=df["numVotes"],
    title="Chart showing the relationship between average rating and the number of Votes of a movie")
    scatterchart.update_layout(
        xaxis_title="Average Rating",
        yaxis_title="Number of Votes"
    )
    scatterchart_html = scatterchart.to_html(full_html=False)
    return render_template("scatterchart.html", scatterchart=scatterchart_html)

@app.route("/piechartold")
def piechartold():
    dfpc = df[["primaryTitle", "numVotes"]]
    dfpc = dfpc.head(10)
    piechartold = px.pie(dfpc, values="numVotes", names="primaryTitle", title="Number of votes of first "
    "10 movies in the list")
    piechartold_html = piechartold.to_html(full_html=False)
    return render_template("piechartold.html", piechartold=piechartold_html)

@app.route("/piechart")
def piechart():
    genrecount = []
    for genre in genresset:
        genrecount.append(genresnew.count(genre))
    dfpc2 = pd.DataFrame({"genres": list(genresset), "count": genrecount})
    piechart = px.pie(dfpc2, values="count", names="genres", title="Popularity of Genres")
    piechart_html = piechart.to_html(full_html=False)
    return render_template("piechart.html", piechart=piechart_html)


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
                Whether a "good movie" should be longer than 2 hour is <b>{await findOpinion()}</b>
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
        
        #print(type(selectedGenres), type(selectedDecade), type(agreement))
        
        
        movieRecommendationHTML = f"""
        <section class="hero is-success">
          <div class="hero-body">
            <p class="title">Based off of your preferences these movies were found in the database</p>
            <p class="is-size-5">{findMovies(selectedGenres, selectedDecade, agreement)}</p>
          </div>
        </section>
        
        """
        return redirect("/form")
        
        # ... code to handle GET requests (e.g., render a form) ...
    return render_template("form.html", formDisabled=formDisabledHTML, historyHero=historyHeroHTML, newHero=heroHTML, movieRecommendation=movieRecommendationHTML)

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
        
async def findDecade():
    chosenDecades = []
    with open("data", "r") as f:
        data = json.load(f)
        for entry in data:
            chosenDecades.append(entry["decade"])
                
    chosenDecadesDF = pd.Series(chosenDecades)
    temp = chosenDecadesDF.mode()[0]
    return temp
async def findOpinion(): 
    chosenOpinion = []
    with open("data", "r") as f:
        data = json.load(f)
        for entry in data:
            chosenOpinion.append(entry["agreement"])                
                
    chosenOpinionDF = pd.Series(chosenOpinion)
    temp = chosenOpinionDF.mode()[0]
    return temp

def findMovies(genres, decade, opinion):
    selectedDF = df[df["startYear"].between(decade, decade + 9)]
    selectedDF.loc[:, "runtimeMinutes"] = pd.to_numeric(selectedDF["runtimeMinutes"], errors="coerce")
    if opinion:
        selectedDF = selectedDF[selectedDF["runtimeMinutes"] > 120]
    else:
        selectedDF = selectedDF[selectedDF["runtimeMinutes"] <= 120]
    #print(selectedDF)
    rowsToAdd = []
    for i in range(len(selectedDF)):
        temp = 0
        for genre in genres:
            if genre in selectedDF.iloc[i, 7]:                   #7 corresponds to genres
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


print(findMovies(["Action", "Adventure", "Family"], 2000, True))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=6006, debug=False)
        
