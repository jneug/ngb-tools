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
        parser_format = request.form.get("parser", "umlet").lower()
        generator_format = request.form.get("generator", "java").lower()

        if parser_format in PARSERS:
            parser = PARSERS[parser_format]()
        else:
            parser = PARSERS["umlet"]()
        classname, attrs, methods = parser.parse(schema)
        if not classname:
            classname = clazz

        if generator_format in GENERATORS:
            generator = GENERATORS[generator_format]()
        else:
            generator = GENERATORS["java"]()
        code = generator.generate_class(classname, attrs, methods)

        return render_template("gettysetty/output.html", code=code, schema=schema)
    else:
        return render_template(
            "gettysetty/input.html",
                generator_formats=GENERATORS.keys(),
                parser_formats=PARSERS.keys()
        )


@bp.route("/download")
def download_file():
    pass
