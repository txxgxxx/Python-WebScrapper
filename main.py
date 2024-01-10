from flask import Flask, render_template

app = Flask("JobScrapper")

@app.route("/")
def home():
    return render_template("home.html", name="taegeon")


@app.route("/hello")
def hello():
    return render_template("home.html")

app.run(port=4000, debug=True)

