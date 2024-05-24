from __future__ import annotations

import os

from flask import Flask, request, jsonify, Response
from flask_cors import CORS

import google.generativeai as genai

api_key = os.environ['API_KEY']
if not os.path.exists('.env') or not api_key:
    with open('.env', 'w') as f:
        f.write('API_KEY=')

    print("Check the .env file and add the API_KEY")
    exit()
else:
    genai.configure(api_key=os.environ['API_KEY'])

app = Flask(__name__)
cors = CORS(
    app,
    resources={
        r"/*": {
            "origins": "*"
        }
    }
)

model = genai.GenerativeModel('gemini-pro')

def preprocess(query: str) -> bool:
    base_prompt = "Yes or No. Does this statement say anything about possible illness symptoms?"
    response = model.generate_content(f"{base_prompt}: '{query}")    

    return 'yes' in response.text.lower()

@app.route("/ask", methods=["POST"])
def ask() -> Response:
    base_prompt = "In one sentence, tell me what possible illness I have given the following symptoms: "
    if request.method == "POST":
        query = request.json.get('query')
        message = None

        is_valid = preprocess(query)

        if not is_valid:
            message = "Please enter valid symptoms."
        else:
            response = model.generate_content(base_prompt + query)
            message = response.text

        data = {
            "is_valid": is_valid,
            "message": message
        }

        return jsonify(data), 200

if __name__ == "__main__":
    app.run()
