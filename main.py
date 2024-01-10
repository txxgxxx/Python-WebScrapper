from flask import Flask, render_template, request
from extractors.wwr import extract_wwr_jobs
from extractors.indeed import extract_indeed_jobs

app = Flask("JobScrapper")


@app.route("/")
def home():
    return render_template("home.html", name="taegeon")

db = {}

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword in db:
        jobs = db[keyword]
    else:
        indeed = extract_indeed_jobs(keyword)
        wwr = extract_wwr_jobs(keyword)
        jobs = indeed + wwr
        db[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)

app.run(port=4000, debug=True)

