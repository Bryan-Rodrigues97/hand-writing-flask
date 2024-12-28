from app import app
from flask import render_template, request, redirect
from AI import recognizer

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def get_itinerary_details():
    data = request.json
    img = data.get("img")

    return recognizer.predict_image_from_base64(img)
    