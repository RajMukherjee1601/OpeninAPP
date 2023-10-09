import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, path)

from flask import Flask, redirect, render_template, request
from flask.helpers import send_file

from backend.request.base import Requests

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/text")
def text():
    return render_template("text.html")


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    prompt = {"user_prompt": input, "mode": "text"}

    req = Requests(prompt)
    return req.handler()


@app.route("/files", methods=["GET", "POST"])
def files():
    if request.method == "POST":
        # Check if a file was uploaded
        if "fileInput" not in request.files:
            return redirect(request.url)

        file = request.files["fileInput"]

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == "":
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Save the uploaded file to the upload folder
            filename = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filename)

            # Process the file (you can add your translation logic here)

            cwd_path = os.getcwd()
            translated_pdf_path = translate_file(filename)
            translated_pdf_path = os.path.join(cwd_path, translated_pdf_path)

            # Serve the translated PDF file for download
            return send_file(translated_pdf_path, as_attachment=True, download_name="translated_output.pdf")

    return render_template("files.html")


def translate_file(filename):
    # Implement your translation logic here
    # You can use libraries like PyPDF2 for PDF files, or other libraries for different file types

    # For demonstration purposes, let's assume you create a translated PDF file
    prompt = {"user_prompt": filename.replace("uploads\\", ""), "mode": "pdf"}

    req = Requests(prompt)
    translated_pdf_content = req.handler()
    print(prompt)
    os.remove(os.path.join(os.getcwd() + "\\uploads\\", prompt["user_prompt"]))
    # Create a temporary directory to store the translated PDF

    translated_pdf_path = os.path.join("converted", "translated_output.txt")

    # Save the translated PDF content to the temporary file
    with open(translated_pdf_path, "w", encoding="utf-8") as pdf_file:
        pdf_file.write(translated_pdf_content)

    # Return the path to the temporary translated PDF file
    return translated_pdf_path


if __name__ == "__main__":
    app.run(debug=True)
