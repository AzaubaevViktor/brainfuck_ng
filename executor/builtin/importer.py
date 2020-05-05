from typing import Type

from lexer import LexerResultT
from ._base import BaseModule


class ModuleImporter:
    @staticmethod
    def scope_with_import():
        module = BaseImportModule()

        return module({})

    @classmethod
    def import_module(cls, ModuleClass: Type['BaseModule'], executor: 'Executor'):
        module = ModuleClass()

        if (dependencies := module.dependencies) is not None:
            for dependency in dependencies:
                if dependency not in BaseModule.modules:
                    raise KeyError(f"Can't resolve dependency {dependency} of {ModuleClass}")
                DependencyClass = BaseModule.modules[dependency]
                cls.import_module(DependencyClass, executor)

        variables = module(executor.variables)

        # TODO: Create new scope / new shadow scope
        executor.variables.update(variables)

        return module


class BaseImportModule(BaseModule):
    NAME = None
    about = "This is base module for import"

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

        return ModuleImporter.import_module(ModuleClass, executor)
