import re


class Parser(object):
    def __init__(self):
        pass

    def parse(self, scheme):
        pass


class UmletParser(Parser):

    _re_name = "([A-Za-z]\S*)"
    _re_types = "((String|int|double|float|boolean|long|short|byte|char|\S+)(\[\])?)"

    # global pattern for matching attributes
    _re_attr = re.compile(f"[+#-]?\s*{_re_name}\s*:\s*{_re_types}(?:\s*=\s*(.+))?")

    # global pattern for matching methods
    _re_meth = re.compile(f"[+#-]?\s*{_re_name}\((.+)?\)\s*:\s*({_re_types}|void)")

    # global pattern for matching classname in umlet scheme
    _re_class = re.compile(f"\*{_re_name}\*")

    # global pattern for matching separator in umlet scheme
    _re_sep = re.compile("--")

    def __init__(self):
        pass

    def parse(self, scheme: str):
        classname = None
        attris = {}
        methods = {}

        lines = scheme.split("\n")
        for line in lines:
            parts = self._re_meth.search(line)
            if parts:
                params = {}

                _name, _params, _type = parts[1], parts[2], parts[3]
                if _params:
                    _params = self._re_attr.findall(_params)
                    for _pname, _ptype, _, _, _ in _params:
                        params[_pname] = _ptype

                modifiers = ["public"]
                if line.startswith("-"):
                    modifiers = ["private"]
                elif line.startswith("#"):
                    modifiers = ["protected"]

                methods[_name] = {
                    "type": _type,
                    "params": params,
                    "modifiers": modifiers,
                }
            else:
                parts = self._re_attr.search(line)
                if parts:
                    _name, _type, _val = parts[1], parts[2], None
                    if parts[5]:
                        _val = parts[5]

                    modifiers = ["private"]
                    if line.startswith("+"):
                        modifiers = ["public"]
                    elif line.startswith("#"):
                        modifiers = ["protected"]

                    attris[_name] = {
                        "type": _type,
                        "value": _val,
                        "modifiers": modifiers,
                    }
                else:
                    parts = self._re_class.search(line)
                    if parts:
                        classname = parts.group(1)

        return classname, attris, methods


class MermaidParser(Parser):

    _re_name = "([A-Za-z]\S*)"
    _re_types = "((String|int|double|float|boolean|long|short|byte|char|\S+)(\[\])?)"

    # global pattern for matching attributes
    _re_attr = re.compile(f"[+#-]?\s*{_re_name}\s*:\s*{_re_types}(?:\s*=\s*(.+))?")

    # global pattern for matching methods
    _re_meth = re.compile(f"[+#-]?\s*{_re_name}\((.+)?\)\s*({_re_types}|void)")

    # global pattern for matching classname in umlet scheme
    _re_class = re.compile(f"class\\v+{_re_name}\\v*{{$")

    def __init__(self):
        pass

    def parse(self, scheme: str):
        classname = None
        attris = {}
        methods = {}

        lines = scheme.split("\n")
        for line in lines:
            parts = self._re_meth.search(line)
            if parts:
                params = {}

                _name, _params, _type = parts[1], parts[2], parts[3]
                if _params:
                    _params = self._re_attr.findall(_params)
                    for _pname, _ptype, _, _, _ in _params:
                        params[_pname] = _ptype

                modifiers = ["public"]
                if line.startswith("-"):
                    modifiers = ["private"]
                elif line.startswith("#"):
                    modifiers = ["protected"]

                methods[_name] = {
                    "type": _type,
                    "params": params,
                    "modifiers": modifiers,
                }
            else:
                parts = self._re_attr.search(line)
                if parts:
                    _name, _type, _val = parts[1], parts[2], None
                    if parts[5]:
                        _val = parts[5]

                    modifiers = ["private"]
                    if line.startswith("+"):
                        modifiers = ["public"]
                    elif line.startswith("#"):
                        modifiers = ["protected"]

                    attris[_name] = {
                        "type": _type,
                        "value": _val,
                        "modifiers": modifiers,
                    }
                else:
                    parts = self._re_class.search(line)
                    if parts:
                        classname = parts.group(1)

        return classname, attris, methods


PARSERS = {"umlet": UmletParser, "mermaid": MermaidParser}
