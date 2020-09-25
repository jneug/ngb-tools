import requests
from flask import Blueprint, request, Response

import html
from urllib.parse import unquote

bp = Blueprint('xmlrpc.api', __name__, template_folder='templates')

@bp.route('/forward', methods=('POST','GET','PUT','DELETE','PATCH'))
def forward():
	to = request.args.get('to', type=str)
	
	resp = requests.request(
		method=request.method,
		url=to,
		headers={key: value for (key, value) in request.headers if key != 'Host'},
		data=request.get_data(),
		cookies=request.cookies,
		allow_redirects=False
	)

	excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
	headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]

	response = Response(resp.content, resp.status_code, headers)
	return response
