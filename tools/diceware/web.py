import requests
from flask import Blueprint, current_app, g, render_template, request, url_for

bp = Blueprint("diceware.web", __name__, template_folder="templates")


@bp.route("/")
def start():
    res = requests.get(url_for("diceware.api.new", _external=True), params={"count": 5})
    if res.status_code == 200:
        passwords = res.text.rstrip().split("\n")
    else:
        passwords = []

    return render_template("diceware/output.html", passwords=passwords)
