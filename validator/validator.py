from flask import Flask, render_template
from db import SolutionLootDB

app = Flask(__name__)
database = SolutionLootDB()

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/raider", methods=["GET"])
def raider():
    raiders = database.list_person()
    return render_template('index.html', people=raiders)

@app.route("/list/<raider>", methods=["GET"])
def lootlist(raider: str):
    lootlist = database.list_lootlist(raider)
    return render_template('lootlist.html', lootlist=lootlist)

if __name__ == "__main__":
    app.run(host='0.0.0.0')