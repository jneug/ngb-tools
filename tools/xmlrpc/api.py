import requests
from requests.auth import HTTPBasicAuth
from flask import Blueprint, request, Response

import html
from urllib.parse import unquote

bp = Blueprint('xmlrpc.api', __name__, template_folder='templates')

@bp.route('/forward', methods=('POST','GET','PUT','DELETE','PATCH'))
def forward():
	data = request.form
	
	url = data['url']
	method = data['method']
	id = data['id']
	content = data['content'].replace('&amp;lt;', '&lt;')
	
	data = f'<?xml version="1.0" encoding="utf-8" standalone="no"?><methodCall><methodName>{method}</methodName><params><param><value><string>{id}</string></value></param><param><value><string>{content}</string></value></param><param><value><array><data/></array></value></param></params></methodCall>'
	
	resp = requests.request(
		method=request.method,
		url=url,
		headers={
			'Content-Type': 'text/xml'
		},
		data=data,
		auth=HTTPBasicAuth(data['username'], data['password'])
	)
	
	response = Response(resp.content, resp.status_code, headers)
	return response
