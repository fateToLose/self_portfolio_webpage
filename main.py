import os
import json
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators
from wtforms.validators import DataRequired, Email

load_dotenv()  # Load environment variables from .env file
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
ref_path: str = os.path.dirname(__file__)

# Email configuration
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", "587"))
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", "true").lower() in ["true", "on", "1"]
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    subject = StringField("Subject", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])


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


@app.route("/contact", methods=["GET", "POST"])
def contact_me():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            # Send email
            msg = Message(
                subject=f"Portfolio Contact: {form.subject.data}",
                sender=os.environ.get("MAIL_DEFAULT_SENDER"),
                recipients=[os.environ.get("RECIPIENT_EMAIL", "your.email@example.com")],
                body=f"""New contact form submission:

Name: {form.name.data}
Email: {form.email.data}
Subject: {form.subject.data}

Message:
{form.message.data}
""",
            )
            mail.send(msg)
            flash("Thank you for your message! I will get back to you soon.", "success")
            return redirect(url_for("contact_me"))
        except Exception as e:
            flash("Sorry, there was an error sending your message. Please try again later.", "error")
            app.logger.error(f"Email sending failed: {str(e)}")

    return render_template("contact_me.html", form=form, active_page="contact")


if __name__ == "__main__":
    app.run(debug=True)
