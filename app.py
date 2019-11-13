from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
import json
import math
import os

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ["MONGODB_URI"]
mongo = PyMongo(app)

@app.before_first_request
def setup():
    # Only for debugging purposes
    # mongo.db.entities.drop()

    my_obj = {}
    with open("result.txt") as f:
        content = f.read()
        my_obj = json.loads(content)

    for user in list(my_obj):
        if mongo.db.entities.find_one({"screen_name": my_obj[user]["screen_name"]}):
            continue
        my_obj[user]["elo"] = 1000
        mongo.db.entities.insert_one(my_obj[user])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/entities")
def get_entities():
    random_entities = list(mongo.db.entities.aggregate([{"$sample": {"size": 2}}]))
    for e in random_entities:
        del e["_id"]
    return jsonify(random_entities)

def probability(r1, r2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (r1 - r2) / 400))

@app.route("/score/<greater>/<lesser>")
def score(greater, lesser):
    # p1 is the winning entity so we must evalute new ELO scores
    player_1 = mongo.db.entities.find_one({"screen_name": greater})
    player_2 = mongo.db.entities.find_one({"screen_name": lesser})

    # safety check
    if player_1 is None or player_2 is None:
        return jsonify({"message": "nice try"})

    p1 = player_1["elo"]
    p2 = player_2["elo"]

    prob_1 = probability(p1,p2)
    prob_2 = probability(p2,p1)

    k = 50

    p1 = p1 + k * (1 - prob_1)
    p2 = p2 + k * (0 - prob_2)

    mongo.db.entities.update_one({"screen_name": greater}, {"$set": {"elo": p1}})
    mongo.db.entities.update_one({"screen_name": lesser}, {"$set": {"elo": p2}})

    return jsonify({"message": "success"})

@app.route("/scoreboard")
def scoreboard():
    entities = list(mongo.db.entities.find())
    entities = sorted(entities, key=lambda x: x["elo"])
    return render_template("scoreboard.html", entities=entities)

if __name__ == "__main__":
    app.run()
