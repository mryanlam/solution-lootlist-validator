from flask import Flask, render_template
from db import SolutionLootDB

app = Flask(__name__)
db = SolutionLootDB()

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/raider", methods=["GET"])
def raider():
    raiders = db.list_person()
    return render_template('index.html', people=raiders)

if __name__ == "__main__":
    app.run(host='0.0.0.0')