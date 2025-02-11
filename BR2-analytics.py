import pandas as pd
import plotly.express as px
from flask import Flask
from flask import render_template
from markupsafe import escape

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

mode = []
for i in genres:
    if genres.count(i) > len(mode):
        mode.append(i)

mode = mode[-1]
print(mode)

#username = input("Enter username: ")

app = Flask(__name__)
@app.route("/")
def work():
    return "website works"

@app.route("/home")
def home():
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
    
@app.route("/piechart")
def piechart():
    dfpc = df[["primaryTitle", "numVotes"]]
    dfpc = dfpc.head(10)
    piechart = px.pie(dfpc, values="numVotes", names="primaryTitle", title="Number of votes of first "
    "10 movies in the list")
    piechart_html = piechart.to_html(full_html=False)
    return render_template("piechart.html", piechart=piechart_html)

@app.route("/form")
def form():
    return render_template("form.html")
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=6006, debug=False)
