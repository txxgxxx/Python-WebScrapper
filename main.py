from flask import Flask

app = Flask("JobScrapper")

@app.route("/")
def home():
    return 'hey there!'

app.run(port=4000, debug=True)

