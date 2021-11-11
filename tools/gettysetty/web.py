from pathlib import Path

from flask import Blueprint, current_app, g, render_template, request

from gettysetty.generator import GENERATORS
from gettysetty.parser import PARSERS

bp = Blueprint("gettysetty.web", __name__, template_folder="templates")


@bp.route("/", methods=("GET", "POST"))
def start():
    if request.method == "POST":
        schema = request.form.get("schema", "")
        clazz = request.form.get("class", "")
        if len(clazz) == 0:
            clazz = "Klasse"
        format = request.form.get("format", "java").lower()

        parser = PARSERS["umlet"]()
        classname, attrs, methods = parser.parse(schema)
        if not classname:
            classname = clazz

        if format in GENERATORS:
            generator = GENERATORS[format]()
        else:
            generator = GENERATORS["java"]()
        code = generator.generate_class(classname, attrs, methods)

        return render_template("gettysetty/output.html", code=code, schema=schema)
    else:
        return render_template(
            "gettysetty/input.html", formats=("java", "latex", "umlet", "mermaid")
        )


@bp.route("/download")
def download_file():
    pass
