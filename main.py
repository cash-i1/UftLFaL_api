from flask import Flask, jsonify, request
import json
import time

app = Flask(__name__)
lb_path = "./lb.json"

default_user = {
    "name": {
        "likes": 0,
        "socials": {
            "youtube": None,
            "discord": None
        },
        "scores": [
            {
                "unix": "20348209320",
                "value": "12",
                "colour": "sd"
            }
        ]
    }
}


# Non routed functions
def lb_json():
    with open(lb_path, "r") as file:
        # data = file.read()
        data = json.load(file)
        return data

def save_json(data):
    with open(lb_path, "w") as file:
        json.dump(data, file, indent=4)

def new_score(unix, value, colour):
    return {
        "unix": unix,
        "value": value,
        "colour": colour
    }

def new_user(name):
    return {
        name: {
            "likes": 0,
            "socials": {},
            "scores": []
        }
    }


# Getters
# Get x users data
@app.route("/get/user/<string:username>")
def get_user_scores(username):
    return get_lb()["users"][username]
        

# Get x top scores
@app.route("/get/top/<int:amount>")
def get_top_scores(amount):
    
    lb = get_lb()
    scores = []
    
    for user in lb["users"]:
        for score in lb["users"][user]["scores"]:
            data = {"user": user, "score": score["value"], "unix": score["unix"], "colour": score["colour"]}

            scores.append(data)
    
    sorted_scores = sorted(scores, key=lambda x: int(x['score']))
    temp = []
    for i, score in enumerate(sorted_scores):
        if i == amount:
            break
        else:
            print(f"{i}/{amount}, {score}")
            temp.append(score) 

    return jsonify(temp)

# Get whole leaderboard
@app.route("/get/lb")
def get_lb():
    return lb_json()

# Setters
@app.route("/<string:set_or_add>/user/<string:username>/<obj>", methods=["POST"])
def set_value(set_or_add, username, obj):
    lb = get_lb()
    score_temp = new_score(time.time(), request.args.get("value"), request.args.get("colour"))

    socials = ""
    if request.args.get("socials"):
        socials = json.loads(request.args.get("socials"))


    if username not in lb["users"]:
        lb["users"].update(new_user(username))

    
    if set_or_add == "set":
        if obj == "score":
            lb["users"][username][obj] = score_temp
       
        if obj == "likes":
            lb["users"][username][obj] = 1
        
        if obj == "socials":
            lb["users"][username][obj] = socials


    elif set_or_add == "add":
        if obj not in lb["users"][username]:
            lb["users"][username][obj] = []

        if obj == "score":
            lb["users"][username][obj].append(score_temp)

        if obj == "likes":
            lb["users"][username][obj] += 1

        if obj == "socials":
            lb["users"][username][obj].update(socials)
    
    print(str(lb)) 
    save_json(lb)
    
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True, port=99182)

