import os
import importlib
import logging

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

	_tools = dir_list = next(os.walk(app.root_path))[1]

	app.tools = {}
	for _tool in sorted(_tools):
		_bp_file = os.path.join(app.root_path, _tool, 'web.py')
		if os.path.isfile(_bp_file):
			try:
				_module = importlib.import_module(f'.{_tool}.web', 'tools')
				app.register_blueprint(_module.bp, url_prefix=f'/{_tool}')
				app.logger.info(f'initialized web module for tool {_tool}')
				app.tools[_tool] = {
					'id': _tool,
					'name': _tool,
					'web': f'{_tool}.web.start',
					'api': None
				}
			except ModuleNotFoundError:
				pass

		_bp_file = os.path.join(app.root_path, _tool, 'api.py')
		if os.path.isfile(_bp_file):
			try:
				_module = importlib.import_module(f'.{_tool}.api', 'tools')
				app.register_blueprint(_module.bp, url_prefix=f'/api/{_tool}')
				app.logger.info(f'initialized api module for tool {_tool}')

				if _tool in app.tools:
					app.tools[_tool]['api'] = f'{_tool}.api.info'
				else:
					app.tools[_tool] = {
						'id': _tool,
						'name': _tool,
						'api': f'{_tool}.api.info',
						'web': None
					}
			except ModuleNotFoundError:
				pass

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
