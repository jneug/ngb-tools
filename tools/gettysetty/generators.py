import re

re_name  = '([A-Za-z]\S*)'
re_types = '(String|int|double|float|boolean|long|short|byte|char|\S+)'

# global pattern for matching attributes
re_attr = re.compile(f'[+-#]?\s*{re_name}\s*:\s*{re_types}(?:\s*=\s*(.+))?')

# global pattern for matching methods
re_meth = re.compile(f'[+-#]?\s*{re_name}\((.+)?\)\s*:\s*({re_types}|void)')

# global pattern for matching classname in umlet scheme
re_class = re.compile(f'\*{re_name}\*')

# global pattern for matching separator in umlet scheme
re_sep = re.compile('--')

# global defaults for attribute values
default_values = {
	'int': '0',
	'boolean': 'false',
	'float': '0.0f',
	'double': '0.0',
	'long': '0L',
	'short': '0',
	'byte': '0',
	'char': '0',
	'String': '""',
	'object': 'null'
}


def indent(depth, text, char='\t'):
	return '\n'.join(map(lambda l: f'{char*depth}{l}', text.split('\n')))
	#return '\n'.join(map(text.split('\n'), lambda l: '{s:{c}^{d}}'.format(l,c=char,d=depth)))

def pCapitalize(name, withp=True):
	if not re.search(r'p[A-Z]', name):
		name = name[0].upper() + name[1:]
		if withp:
			name = 'p' + name
	return name


def gen_var(type, name, modifiers=['private']):
	return f'{" ".join(modifiers)} {type} {name};'

def gen_getter(type, name):
	name_cap = pCapitalize(name, False)
	return f'public {type} get{name_cap}() {{\n\treturn {name};\n}}'

def gen_setter(type, name):
	name_cap = pCapitalize(name, False)
	return f'public void set{name_cap}({type} p{name_cap}) {{\n\t{name} = p{name_cap};\n}}'

def gen_constructor(clazz, attris):
	params = []
	setter = []
	for name,attr in attris.items():
		if attr['value']:
			setter.append(f'\t{name} = {attr["value"]};')
		else:
			params.append(f'{attr["type"]} p{attr["nameCap"]}')
			setter.append(f'\t{name} = p{attr["nameCap"]};')
	params = ', '.join(params)
	setter = '\n'.join(setter)
	return f'public {clazz}({params}) {{\n{setter}\n}}'

def gen_method(type, name, params = {}, modifiers=['public']):
	_params = []
	for pName,pType in params.items():
		_params.append(f'{pType} {pName}')
	params = ', '.join(_params)

	body = ''
	if type != 'void':
		body = indent(1, f'return {default_values[type]};')

	return f'{" ".join(modifiers)} {type} {name}({params}) {{\n{body}\n}}'

def gen_class(clazz, attris, methods):
	vars    = indent(1, '\n'.join([a['var'] for a in attris.values()]))
	funcs   = '\n\n'.join([f"{a['getter']}\n{a['setter']}" for a in attris.values()])
	funcs   = indent(1, funcs)
	constr  = gen_constructor(clazz, attris)
	constr  = indent(1, constr)
	methods = indent(1, '\n\n'.join(m['method'] for m in methods.values()))
	return f'public class {clazz} {{\n\n{vars}\n\n{constr}\n\n{funcs}\n\n{methods}\n\n}}'

def parse_simple(input):
	attris = {}
	lines = input.split('\n')
	for line in lines:
		parts = re_attr.search(line)
		if parts:
			name, type, val = parts[1], parts[2], None
			if parts[3]:
				val = parts[3]

            modifiers = ['private']
            if line.startswith('+'):
                modifiers = ['public']
            elif line.startswith('#'):
                modifiers = ['protected']

			attris[name] = {
				'nameCap': pCapitalize(name, False),
				'type': type,
				'value': val,
				'vis': 'public',
				'var': gen_var(type, name, modifiers=modifiers),
				'getter': gen_getter(type, name),
				'setter': gen_setter(type, name)
			}
	return attris

def parse_umlet(input):
	classname = None
	attris = {}
	methods = {}

	lines = input.split('\n')
	for line in lines:
		parts = re_meth.search(line)
		if parts:
			params = {}

			_name, _params, _type = parts[1], parts[2], parts[3]
			if _params:
				_params = re_attr.findall(_params)
				for _pname, _ptype, _ in _params:
					if not re.search(r'p[A-Z]', _pname):
						_pname = 'p' + _pname[0].upper() + _pname[1:]
					params[_pname] = _ptype

            modifiers = ['public']
            if line.startswith('-'):
                modifiers = ['private']
            elif line.startswith('#'):
                modifiers = ['protected']

			methods[_name] = {
				'type': _type,
				'params': params,
				'method': gen_method(_type, _name, params, modifiers)
			}
		else:
			parts = re_attr.search(line)
			if parts:
				_name, _type, _val = parts[1], parts[2], None
				if parts[3]:
					_val = parts[3]

                modifiers = ['private']
                if line.startswith('+'):
                    modifiers = ['public']
                elif line.startswith('#'):
                    modifiers = ['protected']

				attris[_name] = {
					'nameCap': pCapitalize(_name, False),
					'type': _type,
					'value': _val,
					'vis': 'public',
					'var': gen_var(_type, _name, modifiers),
					'getter': gen_getter(_type, _name),
					'setter': gen_setter(_type, _name)
				}
			else:
				parts = re_class.search(line)
				if parts:
					classname = parts.group(1)

	return classname,attris,methods
