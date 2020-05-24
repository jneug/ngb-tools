import re

# global pattern for matching attributes
re_attr = re.compile('(\S+)\s*:\s*(String|int|double|float|boolean|\S+)(?:\s*=\s*(.+))?')

# global defaults for attribute values
default_values = {
	'int': '0',
	'boolean': 'false',
	'float': '0.0f',
	'double': '0.0',
	'long': '0L',
	'short': '0',
	'object': 'null'
}


def indent(depth, text, char='\t'):
	return '\n'.join(map(lambda l: f'{char*depth}{l}', text.split('\n')))
	#return '\n'.join(map(text.split('\n'), lambda l: '{s:{c}^{d}}'.format(l,c=char,d=depth)))


def gen_var(type, name):
	return f'private {type} {name};'

def gen_getter(type, name):
	name_cap = name.capitalize()
	return f'public {type} get{name_cap}() {{\n\treturn {name};\n}}'

def gen_setter(type, name):
	name_cap = name.capitalize()
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

def gen_class(clazz, attris):
	vars = '\t' + '\n\t'.join([a['var'] for a in attris.values()])
	funcs = '\n\n'.join([f"{a['getter']}\n{a['setter']}" for a in attris.values()])
	funcs = '\t' + funcs.replace('\n', '\n\t')
	constr = gen_constructor(clazz, attris)
	constr = '\t' + constr.replace('\n', '\n\t')
	return f'public class {clazz} {{\n\n{vars}\n\n{constr}\n\n{funcs}\n\n}}'

def parse_simple(input):
	attris = {}
	lines = input.split('\n')
	for line in lines:
		parts = re_attr.search(line)
		if parts:
			name, type, val = parts[1], parts[2], None
			if parts[3]:
				val = parts[3]
			attris[name] = {
				'nameCap': name.capitalize(),
				'type': type,
				'value': val,
				'vis': 'public',
				'var': gen_var(type, name),
				'getter': gen_getter(type, name),
				'setter': gen_setter(type, name)
			}
	return attris
