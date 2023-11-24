import ast

from basel.parsers.parser import Parser


class PythonParser(Parser):
    def get_imports(self, path, native_lib=False, only_local=False):
        with open(path, "r") as module:
            py_tree = ast.parse(module.read())

        _imports = set()
        for stmt in ast.walk(py_tree):
            if isinstance(stmt, ast.Import):
                for alias in stmt.names:
                    _imports.add(alias.name)

            if isinstance(stmt, ast.ImportFrom):
                for alias in stmt.names:
                    if alias.name == "*":
                        _imported_obj = stmt.module
                    else:
                        _imported_obj = f"{stmt.module}.{alias.name}"

                    _imports.add(_imported_obj)

        return list(sorted(_imports))

    @staticmethod
    def _get_ast_value(name: ast.Name):
        return getattr(name, "id", getattr(name, "attr", None))

    def get_classes(self, path):
        with open(path, "r") as module:
            py_tree = ast.parse(module.read())

        _classes = []

        for stmt in ast.walk(py_tree):
            if isinstance(stmt, ast.ClassDef):
                _subclasses = []
                for base in stmt.bases:
                    _subclass = self._get_ast_value(base)
                    _subclasses.append(_subclass)

                _kwargs = {}
                for keyword in stmt.keywords:
                    _kwargs[keyword.arg] = self._get_ast_value(keyword.value)

                _class = (stmt.name, _subclasses, _kwargs)

                _classes.append(_class)

        return _classes

    def is_abstract_class(self, class_name, subclasses, keywords):
        abc_classes = ["abc.ABC", "ABC"]

        if any(subclass in abc_classes for subclass in subclasses):
            return True

        metaclass = keywords.get("metaclass")
        if metaclass in ["ABC", "abc.ABCMeta", "ABCMeta"]:
            return True

        return False
