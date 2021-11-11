from flask import Blueprint, request

from gettysetty.generator import GENERATORS
from gettysetty.parser import PARSERS

bp = Blueprint("gettysetty.api", __name__, template_folder="templates")


@bp.route("/generate", methods=["POST"])
def generate():
    clazz = request.form.get("class", "")
    schema = request.form.get("schema", "")
    parser_format = request.form.get("format", "java").lower()
    generator_format = request.form.get("format", "java").lower()

    if not clazz:
        clazz = "Klasse"

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
    return code
