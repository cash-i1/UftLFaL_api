from flask import Flask, jsonify, request
import json

app = Flask(__name__)
lb_path = "./lb.json"

def lb_json():
    with open(lb_path, "r") as file:
        # data = file.read()
        data = json.load(file)
        return data

@app.route("/get/scores/user/<username>")
def get_user_scores(username):
    pass

@app.route("/get/top/<int:amount>")
def get_top_scores(amount):
    scores = {}
    for i in range(amount):
         

@app.route("/get/lb")
def get_lb():
    return lb_json()

if __name__ == "__main__":
    app.run(debug=True)

