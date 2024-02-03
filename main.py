from flask import Flask, render_template, request, redirect, send_file
from extractors.wwr import extract_wwr_jobs
from extractors.indeed import extract_indeed_jobs
from extractors.ber import extract_ber_jobs
from extractors.web3 import extract_webThree_jobs
from file import save_to_file

app = Flask("JobScrapper")


@app.route("/")
def home():
    return render_template("home.html", name="taegeon")


db = {}


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == (None or ""):
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        berlin = extract_ber_jobs(keyword)
        wwr = extract_wwr_jobs(keyword)
        web3 = extract_webThree_jobs(keyword)
        jobs = berlin + wwr + web3
        db[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)


@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == (None or ""):
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)


# as_attachment 다운로드가 실행되도록 함.

app.run(port=4000, debug=True)
