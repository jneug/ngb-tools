from flask import Blueprint

bp = Blueprint('ytdl.api', __name__, template_folder='templates')

@bp.route('/')
def start():
    return __name__
