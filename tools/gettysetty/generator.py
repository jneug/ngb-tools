import re

from gettysetty.utils import indent, capitalize, pcapitalize, camelcase

# global defaults for attribute values
DEFAULT_VALUES = {
    "int": "0",
    "boolean": "false",
    "float": "0.0f",
    "double": "0.0",
    "long": "0L",
    "short": "0",
    "byte": "0",
    "char": "0",
    "String": '""',
    "object": "null",
}


def default_value(type):
    if type.endswith("[]"):
        t = type[:-2]
        return f"new {t}[10]"
    else:
        return DEFAULT_VALUES[type]


def is_array(type):
    return type.endswith("[]")


def base_type(type):
    t = type
    if is_array(t):
        t = t[:-2]
    if t in DEFAULT_VALUES.keys():
        return t
    else:
        return "object"


class Generator(object):
    def __init__(self):
        self._normalize_names = False

    def sort_by_name(self):
        self._sorting = "name"

    def group_by_type(self):
        self._grouping = "type"

    def set_normalize_names(self, bln):
        self._normalize_names = bln

    def generate_class(name, attris, methods):
        pass


class JavaGenerator(Generator):
    def __init__(self, indent_char="\t", gen_array=False, getset_group_by="attribute"):
        self._indent_char = indent_char
        self._gen_array = gen_array
        self._getset_group_by = getset_group_by

    def gen_classname(self, name):
        return capitalize(camelcase(name))

    def gen_var(self, type, name, modifiers=["private"]):
        return f'{" ".join(modifiers)} {type} {name};'

    def gen_getter(self, type, name):
        name_cap = capitalize(name)
        return (
            f"public {type} get{name_cap}() {{\n{self._indent_char}return {name};\n}}"
        )

    def gen_setter(self, type, name):
        name_cap = capitalize(name)
        return f"public void set{name_cap}({type} p{name_cap}) {{\n{self._indent_char}{name} = p{name_cap};\n}}"

    def gen_array_getter(self, type, name):
        btype = base_type(type)
        name_cap = capitalize(name)
        return f"public {btype} get{name_cap}(int pIndex) {{\n{self._indent_char}return {name}[pIndex];\n}}"

    def gen_array_setter(self, type, name):
        btype = base_type(type)
        name_cap = capitalize(name)
        return f"public void set{name_cap}(int pIndex, {btype} p{name_cap}) {{\n{self._indent_char}{name}[pIndex] = p{name_cap};\n}}"

    def gen_constructor(self, clazz, attris):
        params = []
        setter = []
        for name, attr in attris.items():
            if attr["value"]:
                setter.append(f'{self._indent_char}{name} = {attr["value"]};')
            else:
                name_cap = capitalize(name)
                params.append(f'{attr["type"]} p{name_cap}')
                setter.append(f"{self._indent_char}{name} = p{name_cap};")
        params = ", ".join(params)
        setter = "\n".join(setter)
        return f"public {clazz}({params}) {{\n{setter}\n}}"

    def gen_method(self, type, name, params={}, modifiers=["public"]):
        _params = []
        for pName, pType in params.items():
            pName = pcapitalize(pName)
            _params.append(f"{pType} {pName}")
        params = ", ".join(_params)

        body = ""
        if type != "void":
            body = indent(1, f"return {default_value(type)};", char=self._indent_char)

        return f'{" ".join(modifiers)} {type} {name}({params}) {{\n{body}\n}}'

    def generate_class(self, clazz, attris, methods):
        vars = list()
        getters = list()
        setters = list()
        funcs = list()
        constr = ""

        cname = self.gen_classname(clazz)

        for name, attr in attris.items():
            vars.append(self.gen_var(attr["type"], name, attr["modifiers"]))

            g = self.gen_getter(attr["type"], name)
            if self._getset_group_by == "type":
                getters.append(g)
            else:
                funcs.append(g)
            s = self.gen_setter(attr["type"], name)
            if self._getset_group_by == "type":
                setters.append(s)
            else:
                funcs.append(s)

            if is_array(attr["type"]) and self._gen_array:
                funcs.append(self.gen_array_getter(attr["type"], name))
                funcs.append(self.gen_array_setter(attr["type"], name))

        constr = self.gen_constructor(cname, attris)

        for name, m in methods.items():
            funcs.append(self.gen_method(m["type"], name, m["params"], m["modifiers"]))

        vars = indent(1, "\n".join(vars), char=self._indent_char)
        funcs = indent(
            1, "\n\n".join(getters + setters + funcs), char=self._indent_char
        )
        constr = indent(1, constr, char=self._indent_char)

        return f"public class {cname} {{\n\n{vars}\n\n{constr}\n\n{funcs}\n\n}}"


class LatexGenerator(Generator):
    pass


class TikzGenerator(Generator):
    pass


class UmletGenerator(Generator):
    def __init__(self, gen_array=False, getset_group_by="attribute"):
        self._gen_array = gen_array
        self._getset_group_by = getset_group_by

    def _get_visibility(self, modifiers, default="-"):
        if "public" in modifiers:
            return "+"
        elif "protected" in modifiers:
            return "#"
        elif "private" in modifiers:
            return "-"
        else:
            return default

    def gen_classname(self, name):
        return capitalize(camelcase(name))

    def gen_var(self, type, name, modifiers=["private"]):
        vis = self._get_visibility(modifiers)
        return f"{vis}{name}: {type}"

    def gen_getter(self, type, name):
        name_cap = capitalize(name)
        return f"+get{name_cap}(): {type}"

    def gen_setter(self, type, name):
        name_cap = capitalize(name)
        return f"+set{name_cap}(p{name_cap}: {type}): void"

    def gen_array_getter(self, type, name):
        btype = base_type(type)
        name_cap = capitalize(name)
        return f"+get{name_cap}(pIndex: int): {btype}"

    def gen_array_setter(self, type, name):
        btype = base_type(type)
        name_cap = capitalize(name)
        return f"+set{name_cap}(pIndex: int, p{name_cap}: {btype}): void"

    def gen_constructor(self, clazz, attris):
        params = []
        for name, attr in attris.items():
            if not attr["value"]:
                pName = pcapitalize(name)
                params.append(f'{pName}: {attr["type"]}')
        params = ", ".join(params)
        return f"+{clazz}({params})"

    def gen_method(self, type, name, params={}, modifiers=["public"]):
        _params = []
        for pName, pType in params.items():
            pName = pcapitalize(pName)
            _params.append(f"{pName}: {pType}")
        params = ", ".join(_params)
        vis = self._get_visibility(modifiers, default="+")

        return f"{vis}{name}({params}): {type}"

    def generate_class(self, clazz, attris, methods):
        vars = list()
        getters = list()
        setters = list()
        funcs = list()
        constr = ""

        cname = self.gen_classname(clazz)

        for name, attr in attris.items():
            vars.append(self.gen_var(attr["type"], name, attr["modifiers"]))

            g = self.gen_getter(attr["type"], name)
            if self._getset_group_by == "type":
                getters.append(g)
            else:
                funcs.append(g)
            s = self.gen_setter(attr["type"], name)
            if self._getset_group_by == "type":
                setters.append(s)
            else:
                funcs.append(s)

            if is_array(attr["type"]) and self._gen_array:
                funcs.append(self.gen_array_getter(attr["type"], name))
                funcs.append(self.gen_array_setter(attr["type"], name))

        constr = self.gen_constructor(cname, attris)

        for name, m in methods.items():
            funcs.append(self.gen_method(m["type"], name, m["params"], m["modifiers"]))

        vars = "\n".join(vars)
        funcs = "\n".join(getters + setters + funcs)

        return f"*{cname}*\n--\n{vars}\n--\n{constr}\n{funcs}"


class MermaidGenerator(Generator):
    def __init__(self, indent_char="\t", gen_array=False, getset_group_by="attribute"):
        self._indent_char = indent_char
        self._gen_array = gen_array
        self._getset_group_by = getset_group_by

    def _get_visibility(self, modifiers, default="-"):
        if "public" in modifiers:
            return "+"
        elif "protected" in modifiers:
            return "#"
        elif "private" in modifiers:
            return "-"
        else:
            return default

    def gen_classname(self, name):
        return capitalize(camelcase(name))

    def gen_var(self, type, name, modifiers=["private"]):
        vis = self._get_visibility(modifiers)
        return f"{vis}{name}: {type}"

    def gen_getter(self, type, name):
        name_cap = capitalize(name)
        return f"+get{name_cap}() {type}"

    def gen_setter(self, type, name):
        name_cap = capitalize(name)
        return f"+set{name_cap}(p{name_cap}: {type}) void"

    def gen_array_getter(self, type, name):
        btype = base_type(type)
        name_cap = capitalize(name)
        return f"+get{name_cap}(pIndex: int) {btype}"

    def gen_array_setter(self, type, name):
        btype = base_type(type)
        name_cap = capitalize(name)
        return f"+set{name_cap}(pIndex: int, p{name_cap}: {btype}) void"

    def gen_constructor(self, clazz, attris):
        params = []
        for name, attr in attris.items():
            if not attr["value"]:
                pName = pcapitalize(name)
                params.append(f'{pName}: {attr["type"]}')
        params = ", ".join(params)
        return f"+{clazz}({params})"

    def gen_method(self, type, name, params={}, modifiers=["public"]):
        _params = []
        for pName, pType in params.items():
            pName = pcapitalize(pName)
            _params.append(f"{pName}: {pType}")
        params = ", ".join(_params)
        vis = self._get_visibility(modifiers, default="+")

        return f"{vis}{name}({params}) {type}"

    def generate_class(self, clazz, attris, methods):
        vars = list()
        getters = list()
        setters = list()
        funcs = list()
        constr = ""

        cname = self.gen_classname(clazz)

        for name, attr in attris.items():
            vars.append(self.gen_var(attr["type"], name, attr["modifiers"]))

            g = self.gen_getter(attr["type"], name)
            if self._getset_group_by == "type":
                getters.append(g)
            else:
                funcs.append(g)
            s = self.gen_setter(attr["type"], name)
            if self._getset_group_by == "type":
                setters.append(s)
            else:
                funcs.append(s)

            if is_array(attr["type"]) and self._gen_array:
                funcs.append(self.gen_array_getter(attr["type"], name))
                funcs.append(self.gen_array_setter(attr["type"], name))

        for name, m in methods.items():
            funcs.append(self.gen_method(m["type"], name, m["params"], m["modifiers"]))

        vars = indent(1, "\n".join(vars), char=self._indent_char)
        constr = indent(1, self.gen_constructor(cname, attris), char=self._indent_char)
        funcs = indent(1, "\n".join(getters + setters + funcs), char=self._indent_char)

        return f"class {cname} {{\n{vars}\n\n{constr}\n{funcs}\n}}"


GENERATORS = {
    "umlet": UmletGenerator,
    "java": JavaGenerator,
    "mermaid": MermaidGenerator,
}
