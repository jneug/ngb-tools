from flask import Blueprint, request

import gettysetty.generator as generator
import gettysetty.parser as parser

bp = Blueprint("gettysetty.api", __name__, template_folder="templates")


@bp.route("/generate", methods=["POST"])
def generate():
    clazz = request.form.get("class", "")
    schema = request.form.get("schema", "")
    format = request.form.get("format", "java").lower()

    if not clazz:
        clazz = "Klasse"

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
    return code
