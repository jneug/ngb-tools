import os
import importlib
import logging
import pkgutil

from flask import Flask, render_template, url_for, request


def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev'
	)

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)


	# setup gunicorn logging
	# See: https://trstringer.com/logging-flask-gunicorn-the-manageable-way/
	if app.env == 'production':
		gunicorn_logger = logging.getLogger('gunicorn.error')
		app.logger.handlers = gunicorn_logger.handlers
		app.logger.setLevel(gunicorn_logger.level)

	# ensure the instance folder exists
	folders = [ app.instance_path ]
	for f in folders:
		try:
			os.makedirs(f)
		except OSError:
			pass

	app.tools = {}
	for loader, module_name, is_pkg in  pkgutil.walk_packages(__path__):
		if is_pkg:
			_module = loader.find_module(module_name).load_module(module_name)

			if getattr(_module, 'active', True):
				_tool = {
					'id': module_name,
					'name': _module.name if hasattr(_module, 'name') else module_name,
					'description': _module.description if hasattr(_module, 'description') else '',
					'web': None,
					'api': None
				}

				if hasattr(_module, 'web'):
					app.register_blueprint(_module.web.bp, url_prefix=f'/{module_name}')

					web_start = 'start'
					if hasattr(_module, 'web_start'):
						web_start = _module.web_start
					_tool['web'] =  f'{module_name}.web.{web_start}'

					app.logger.info(f'initialized web module for tool {module_name}')

				if hasattr(_module, 'api'):
					app.register_blueprint(_module.api.bp, url_prefix=f'/api/{module_name}')

					_tool['api'] = f'{module_name}.api.info'

					app.logger.info(f'initialized api module for tool {module_name}')

				if _tool['web'] or _tool['api']:
					app.tools[_tool['id']] = _tool

	# Add default route for index page
	@app.route('/')
	def start():
		return render_template('index.html', tools=app.tools)

	@app.context_processor
	def current_tool():
		_tool = request.path[1:-1]
		if _tool in app.tools:
			return dict(tool=app.tools[_tool])
		else:
			return dict(tool=None)

	return app
