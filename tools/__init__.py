import os
import importlib

from flask import Flask, render_template, url_for


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

	# ensure the instance folder exists
	folders = [ app.instance_path ]
	for f in folders:
		try:
			os.makedirs(f)
		except OSError:
			pass

	_tools = dir_list = next(os.walk(app.root_path))[1]

	tools = {}
	for _tool in _tools:
		_bp_file = os.path.join(app.root_path, _tool, 'web.py')
		if os.path.isfile(_bp_file):
			try:
				_module = importlib.import_module(f'.{_tool}.web', 'tools')
				app.register_blueprint(_module.bp, url_prefix=f'/{_tool}')
				app.logger.info(f'initialized web module for tool {_tool}')
				tools[_tool] = {
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

				if _tool in tools:
					tools[_tool]['api'] = f'{_tool}.api.start'
				else:
					tools[_tool] = {
						'name': _tool,
						'api': f'{_tool}.api.start',
						'web': None
					}
			except ModuleNotFoundError :
				pass

	# Add default route for index page
	@app.route('/')
	def start():
		return render_template('index.html', tools=tools)

	return app
