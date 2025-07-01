from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["github_events"]
collection = db["events"]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')

    if event_type == 'push':
        author = data['pusher']['name']
        branch = data['ref'].split('/')[-1]
        timestamp = datetime.utcnow().strftime('%d %B %Y - %I:%M %p UTC')
        message = f'"{author}" pushed to "{branch}" on {timestamp}'

    elif event_type == 'pull_request':
        action = data['action']
        if action in ['opened', 'reopened']:
            author = data['pull_request']['user']['login']
            from_branch = data['pull_request']['head']['ref']
            to_branch = data['pull_request']['base']['ref']
            timestamp = datetime.utcnow().strftime('%d %B %Y - %I:%M %p UTC')
            message = f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}'
        elif action == 'closed' and data['pull_request']['merged']:
            author = data['pull_request']['user']['login']
            from_branch = data['pull_request']['head']['ref']
            to_branch = data['pull_request']['base']['ref']
            timestamp = datetime.utcnow().strftime('%d %B %Y - %I:%M %p UTC')
            message = f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp}'
        else:
            return '', 204
    else:
        return '', 204

    collection.insert_one({"message": message, "timestamp": datetime.utcnow()})
    return jsonify({"status": "ok"}), 200

@app.route('/events')
def get_events():
    events = list(collection.find().sort("timestamp", -1).limit(10))
    return jsonify([{"message": e["message"]} for e in events])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
