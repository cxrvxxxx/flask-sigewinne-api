import pathlib
import textwrap
import threading
import os

from flask import Flask, request, jsonify
from flask_cors import CORS

import google.generativeai as genai
api_key = os.environ['API_KEY']
if not os.path.exists('.env') or not api_key:
    with open('.env', 'w') as f:
        f.write('API_KEY=')

    print("Check the .env file and add the API_KEY")
    exit()
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

@app.route("/ask", methods=["POST"])
def ask():
    base_prompt = "In one sentence, tell me what possible illness I have given the following symptoms: "
    if request.method == "POST":
        query = request.json.get('query')
        message = None

        if not query:
            message = "Please enter valid symptooms."
        else:
            response = model.generate_content(base_prompt + query)
            message = response.text

        return jsonify({"message": message}), 200

if __name__ == "__main__":
    app.run()
