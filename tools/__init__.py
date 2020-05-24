import os
import importlib

from flask import Flask


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

	#from .gettysetty import web
	#app.register_blueprint(web.bp, url_prefix='/gettysetty')

	_tools = dir_list = next(os.walk(app.root_path))[1]
	#_tools = filter(lambda d: os.path.isfile(os.path.join(app.root_path,d,'web.py')), _tools)

	for _tool in _tools:
		_bp_file = os.path.join(app.root_path, _tool, 'web.py')
		if os.path.isfile(_bp_file):
			_module = importlib.import_module(f'.{_tool}.web', 'tools')
			app.register_blueprint(_module.bp, url_prefix=f'/{_tool}')
			app.logger.info(f'initialized tool {_tool}')

	return app
