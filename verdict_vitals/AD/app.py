from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import pickle
from models.model import load_model, generate_summary
import os

app = Flask(__name__)

tokenizer, model = load_model()

HISTORY_FILE = "history.pkl"
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "rb") as f:
        history = pickle.load(f)
else:
    history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/summary", methods=["GET", "POST"])
def summary():
    if request.method == "POST":
        try:
            text = request.form.get("text")

            if not text:
                return jsonify({"error": "No text provided"}), 400

            summary_text = generate_summary(text, tokenizer, model)
            session['summary'] = summary_text
            history.append({"input": text, "summary": summary_text})
            with open(HISTORY_FILE, "wb") as f:
                pickle.dump(history, f)
            return jsonify({"redirect": url_for("summary_result")})

        except Exception as e:
            print("Error:", str(e))
            return jsonify({"error": "Something went wrong"}), 500

    return render_template("summary.html")

@app.route("/summary-result")
def summary_result():
    summary_text = session.get('summary', '')
    return render_template("summary_result.html", summary=summary_text)

if __name__ == "__main__":
    app.run(debug=True)
