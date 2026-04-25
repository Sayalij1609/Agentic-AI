from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# ------------------------
# LOAD DATASET
# ------------------------

df = pd.read_csv("Online_Courses.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Select required columns
df = df[
[
"Course Title",
"Category",
"Skills",
"Level",
"Short Intro",
"URL",
"Site",
"Duration"
]
]

# Rename columns
df.columns = [
"course_title",
"category",
"skills",
"level",
"description",
"url",
"site",
"duration"
]

df = df.fillna("")

# Feature engineering
df["features"] = (
df["skills"]+" "+
df["category"]+" "+
df["level"]+" "+
df["description"]
)

# ------------------------
# TFIDF MODEL
# ------------------------

vectorizer = TfidfVectorizer(
stop_words="english"
)

matrix = vectorizer.fit_transform(
df["features"]
)

similarity = cosine_similarity(
matrix
)

# ------------------------
# HOME
# ------------------------

@app.route("/")
def home():

    courses = sorted(
        df["course_title"]
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )

    return render_template(
        "index.html",
        courses=courses
    )


# ------------------------
# RECOMMEND
# ------------------------

@app.route("/recommend",methods=["POST"])
def recommend():

    selected_course=request.form.get("course")
    keyword=request.form.get("keyword")


    # --------------------
    # MANUAL KEYWORD SEARCH
    # --------------------
    if keyword and keyword.strip()!="":

        filtered=df[
            df["features"].str.contains(
                keyword,
                case=False,
                na=False
            )
        ].head(5)

        results=[]

        for _,rec in filtered.iterrows():

            results.append({
            "course":rec["course_title"],
            "platform":rec["site"],
            "duration":rec["duration"],
            "link":rec["url"],
            "category":rec["category"],
            "skills":rec["skills"],
            "level":rec["level"],
            "description":rec["description"],
            "score":"Keyword Match",
            "reason":"Recommended based on searched skill"
            })

        return render_template(
            "result.html",
            selected=keyword,
            results=results
        )


    # --------------------
    # COURSE BASED RECOMMENDATION
    # --------------------

    idx=df[
        df["course_title"]==selected_course
    ].index[0]

    scores=sorted(
        list(enumerate(similarity[idx])),
        key=lambda x:x[1],
        reverse=True
    )[1:6]

    results=[]

    for i,score in scores:

        rec=df.iloc[i]

        reasons=[]

        if rec["level"]==df.iloc[idx]["level"]:
            reasons.append(
                "Same difficulty level"
            )

        if rec["category"]==df.iloc[idx]["category"]:
            reasons.append(
                "Same category"
            )

        if len(reasons)==0:
            reasons.append(
                "High content similarity"
            )


        results.append({
        "course":rec["course_title"],
        "platform":rec["site"],
        "duration":rec["duration"],
        "link":rec["url"],
        "category":rec["category"],
        "skills":rec["skills"],
        "level":rec["level"],
        "description":rec["description"],
        "score":round(score*100,2),
        "reason":" | ".join(reasons)
        })



    return render_template(
        "result.html",
        selected=selected_course,
        results=results
    )


# ------------------------
# RUN
# ------------------------

if __name__=="__main__":
    app.run(debug=True)