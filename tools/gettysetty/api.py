from flask import Blueprint, request

from gettysetty.generators import gen_class, parse_umlet

bp = Blueprint("gettysetty.api", __name__, template_folder="templates")


@bp.route("/generate", methods=["POST"])
def generate():
    clazz = request.form.get("class", "")
    schema = request.form.get("schema", "")

    if not clazz:
        clazz = "Klasse"

    classname, attrs, methods = parse_umlet(schema)
    if not classname:
        classname = clazz

    code = gen_class(classname, attrs, methods)
    return code
