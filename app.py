from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os
from ecombot.retrieval_generation import generation
from ecombot.ingest import ingestdata

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Safely ingest data and build the chain
try:
    vstore, *_ = ingestdata("done")  # ✅ Proper unpacking
    chain = generation(vstore)
except Exception as e:
    print(f"[ERROR] Failed to initialize vector store or chain: {e}")
    chain = None

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get", methods=["GET", "POST"])
def chat():
    if not chain:
        return jsonify({"error": "The chatbot is not available at the moment. Please try again later."}), 500

    try:
        msg = request.form["msg"]
        result = chain.invoke(msg)
        print("Response:", result)
        return str(result)
    except Exception as e:
        print(f"[ERROR] During chat handling: {e}")
        return jsonify({"error": "Something went wrong while processing your request."}), 500

if __name__ == '__main__':
    app.run(debug=True)
