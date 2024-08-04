from webApp import app, vision
from flask import render_template

@app.route("/")
def index():
    vision.clear()
    return render_template("index.pug")