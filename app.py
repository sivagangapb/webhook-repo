from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB Atlas Connection
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["webhook"]
collection = db["events"]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    ist = pytz.timezone('Asia/Kolkata')
    timestamp = datetime.now(ist).strftime('%d %B %Y - %I:%M %p IST')

    if event_type == 'push':
        author = data['pusher']['name']
        branch = data['ref'].split('/')[-1]
        message = f'"{author}" pushed to "{branch}" on {timestamp}'

    elif event_type == 'pull_request':
        action = data['action']
        author = data['pull_request']['user']['login']
        from_branch = data['pull_request']['head']['ref']
        to_branch = data['pull_request']['base']['ref']

        if action in ['opened', 'reopened']:
            message = f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}'
        elif action == 'closed' and data['pull_request']['merged']:
            message = f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp}'
        else:
            return '', 204
    else:
        return '', 204

    collection.insert_one({"message": message, "timestamp": timestamp})
    return jsonify({"status": "ok"}), 200

@app.route('/events')
def get_events():
    events = list(collection.find().sort("timestamp", -1).limit(10))
    return jsonify([{"message": e["message"], "timestamp": e["timestamp"]} for e in events])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
