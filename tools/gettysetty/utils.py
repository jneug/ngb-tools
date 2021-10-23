import re
import typing as t


def indent(depth: int, text: str, char: str = '\t') -> str:
    return '\n'.join(map(lambda l: f'{char*depth}{l}', text.split('\n')))
    #return '\n'.join(map(text.split('\n'), lambda l: '{s:{c}^{d}}'.format(l,c=char,d=depth)))


def camelcase(name: str) -> str:
    return re.sub(r'(\s+|_|-)(\S)', lambda m: m.group(2).upper(), name.strip())


def normalize_java(name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9$_]', '', re.sub(r'^[^a-zA-Z]*', '', name))


def capitalize(name: str) -> str:
    """Capitalize string, but keep camel case intact."""
    return name[0].upper() + name[1:]


def pcapitalize(name: str) -> str:
    if not re.search(r'^p[A-Z]', name):
        name = capitalize(name)
    return f'p{name}'
