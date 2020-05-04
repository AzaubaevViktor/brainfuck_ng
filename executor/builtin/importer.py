from typing import Type

from ._base import BaseModule, BaseImportModule


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
                DependencyClass = BaseModule.modules[dependency]
                cls.import_module(DependencyClass, executor)

        variables = module(executor.variables)

        # TODO: Create new scope / new shadow scope
        executor.variables.update(variables)

        return module
