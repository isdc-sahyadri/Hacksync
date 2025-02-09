from flask import Flask, request, render_template, jsonify
import os
from plagiarism_checker import PlagiarismChecker

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

plagiarism_checker = PlagiarismChecker()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    similarity_score, message, extracted_text = plagiarism_checker.check_plagiarism(filepath, UPLOAD_FOLDER)

    if "Error" in extracted_text:
        return jsonify({"error": extracted_text}), 400

    return jsonify({
        "similarity_score": similarity_score,
        "message": message
    })

if __name__ == "__main__":
    app.run(debug=True)
