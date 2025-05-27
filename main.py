import os
import json
from flask import Flask, render_template

app = Flask(__name__)
ref_path: str = os.path.dirname(__file__)


def load_json_data(filename):
    filepath = os.path.join(ref_path, "data", filename)
    with open(filepath, "r") as file:
        return json.load(file)


@app.route("/")
def home():
    profile = load_json_data("profile.json")
    cv = load_json_data("cv.json")
    return render_template("landing_page.html", profile=profile, cv=cv, active_page="home")


@app.route("/portfolio")
def portfolio_page():
    projects = load_json_data("projects.json")
    return render_template("portfolio.html", projects=projects, active_page="portfolio")


@app.route("/photo_showcase")
def photo_showcase_page():
    photos = load_json_data("photo.json")
    return render_template("photo_showcase.html", photos=photos, active_page="photo_showcase")


@app.route("/contact")
def contact_me():
    return render_template("contact_me.html", active_page="contact")


if __name__ == "__main__":
    app.run(debug=True)
