from pathlib import Path

from flask import Blueprint, current_app, g, render_template, request

# from .generators import gen_class, parse_umlet
import gettysetty.generator as generator
import gettysetty.parser as parser

bp = Blueprint("gettysetty.web", __name__, template_folder="templates")


@bp.route("/", methods=("GET", "POST"))
def start():
    if request.method == "POST":
        schema = request.form.get("schema", "")
        clazz = request.form.get("class", "")
        if len(clazz) == 0:
            clazz = "Klasse"
        format = request.form.get("format", "java").lower()

        p = parser.UmletParser()
        classname, attrs, methods = p.parse(schema)
        if not classname:
            classname = clazz

        if format == "latex":
            g = generator.LatexGenerator()
        elif format == "umlet":
            g = generator.UmletGenerator()
        elif format == "mermaid":
            g = generator.MermaidGenerator()
        else:
            g = generator.JavaGenerator()
        code = g.generate_class(classname, attrs, methods)

        return render_template("gettysetty/output.html", code=code, schema=schema)
    else:
        return render_template(
            "gettysetty/input.html", formats=("java", "latex", "umlet", "mermaid")
        )


@bp.route("/download")
def download_file():
    pass
