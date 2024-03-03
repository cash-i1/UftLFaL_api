from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/get-user/<user_id>")
def get_user(user_id):
    user_data = {
        "user_id": user_id,
        "name": "JOHM",
        "email": "asdfsdf@sdf.com"
    }

    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra

    return jsonify(user_data), 200

@app.route("/create-user", methods=["POST"])
def create_user():
    if request.method == "POST":
        data = request.get_json()

        return 201

if __name__ == "__main__":
    app.run(debug=True)