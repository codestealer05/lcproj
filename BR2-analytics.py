import pandas as pd
import plotly.express as px
from flask import Flask

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

fig = px.scatter(x=df["averageRating"], y=df["numVotes"])
fig.update_layout(
    xaxis_title="Average Rating",
    yaxis_title="Number of Votes"
)
fig.show()


app = Flask(__name__)
@app.route("/")
def hello():
    return "hello"
@app.route("/scatterchart")
def chart():
    return fig.show()
    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=6006, debug=False)
