from typing import Type

from ._base import BaseModule, BaseImportModule


class ModuleImporter:
    @property
    def scope_with_import(self):
        module = BaseImportModule(self)

        return module({})

    def import_module(self, ModuleClass: Type['BaseModule'], executor: 'Executor'):
        module = ModuleClass()

        if (dependencies := module.dependencies) is not None:
            for dependency in dependencies:
                DependencyClass = BaseModule.modules[dependency]
                self.import_module(DependencyClass, executor)


        variables = module(executor.variables)

        # TODO: Create new scope / new shadow scope
        executor.variables.update(variables)

        return module
