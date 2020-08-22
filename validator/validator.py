from flask import Flask, render_template, request
from db import SolutionLootDB
from validate_sheet import validate_sheet

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

@app.route("/validate",  methods=["GET", "POST"])
def validate_sheet():
    uri = request.args.get('uri')
    c = request.args.get('class')
    try:
        valid, err_msg_dict = (validate_sheet(c, uri))
        return render_template('lootlist.html', valid=valid, error=err_msg_dict)
    except Exception as e:
        return render_template('lootlist.html', fail=e)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
