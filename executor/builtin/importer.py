from typing import Type

from executor.builtin._import import BaseImportModule


class ModuleImporter:
    @property
    def scope_with_import(self):
        module = BaseImportModule(self)

        return module({})

    def import_module(self, ModuleClass: Type['BaseModule'], executor: 'Executor'):
        module = ModuleClass()

        variables = module(executor.variables)

        # TODO: Create new scope / new shadow scope
        executor.variables.update(variables)

        return module
