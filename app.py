from flask import Flask, request, jsonify
from flask_cors import CORS
from model import generate_follow_up
from utils import get_timestamp, get_device_info

app = Flask(__name__)
CORS(app)

surveys = {}  # temporary in-memory survey store
responses = []  # temporary in-memory responses

@app.route("/")
def home():
    return jsonify({"message": "AI Survey Tool is live 🚀"})

@app.route("/api/create_survey", methods=["POST"])
def create_survey():
    data = request.json
    survey_id = data.get("id")
    surveys[survey_id] = data
    return jsonify({"status": "success", "message": "Survey created", "survey_id": survey_id})

@app.route("/api/fetch_survey/<survey_id>", methods=["GET"])
def fetch_survey(survey_id):
    survey = surveys.get(survey_id)
    if not survey:
        return jsonify({"error": "Survey not found"}), 404
    return jsonify(survey)

@app.route("/api/submit_response", methods=["POST"])
def submit_response():
    data = request.json
    response_data = {
        "timestamp": get_timestamp(),
        "device": get_device_info(request),
        "response": data
    }
    responses.append(response_data)
    return jsonify({"status": "success", "message": "Response submitted"})

@app.route("/api/suggest_follow_up", methods=["POST"])
def suggest_follow_up():
    answer = request.json.get("answer")
    follow_up = generate_follow_up(answer)
    return jsonify({"follow_up": follow_up})

if __name__ == "__main__":
    app.run(debug=True)
