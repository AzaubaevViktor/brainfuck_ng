from typing import Dict, Type

from lexer import LexerResultT


class BaseModule:
    NAME = None
    about = "This is base module, please inherit from them"

    modules: Dict[str, Type["BaseModule"]] = {}

    dependencies = None

    def __init_subclass__(cls, **kwargs):
        print("Register this please:", cls, kwargs)
        if cls.NAME:
            cls.modules[cls.NAME] = cls

    def __call__(self, variables):
        raise NotImplementedError()

    def shutdown(self):
        # Not realized in executor, sorry
        raise NotImplementedError()


class BaseImportModule(BaseModule):
    NAME = None
    about = "This is base module for import"

    def __init__(self):
        from .importer import ModuleImporter
        self.importer = ModuleImporter

    def __call__(self, variables):
        return {
            'import:@modules': self.modules,
            'import:builtin': self._do_import,
            'import:scan': self._do_scan,
        }

    def _do_scan(self, path: LexerResultT, executor):
        # TODO: This is fake
        raise NotImplementedError()

    def _do_import(self, name, executor):
        module_name = name.text

        assert module_name in self.modules, self.modules

        ModuleClass = self.modules[module_name]

        return self.importer.import_module(ModuleClass, executor)
