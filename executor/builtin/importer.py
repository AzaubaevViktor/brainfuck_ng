from typing import Type

from lexer import LexerResultT, Lemma, FileSource
from ._base import BaseModule
from .. import ExecutorError, ErrorStackFrame


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
            'import:builtin': self._do_import_builtin,
            'import:builtin:inline': self._do_import_builtin_inline,
            'import': self._do_import,
            'import:inline': self._do_import_inline,
            'import:scan': self._do_scan,
        }

    def _do_scan(self, path: LexerResultT, executor):
        # TODO: This is fake
        raise NotImplementedError()

    def _do_import_builtin_inline(self, name, executor: "Executor"):
        module_name = name.text

        assert module_name in self.modules, self.modules

        ModuleClass = self.modules[module_name]

        return ModuleImporter.import_module(ModuleClass, executor)

    def _do_import_builtin(self, name: Lemma, commands: LexerResultT = None, *, executor):
        module_name = name.text

        if module_name not in self.modules:
            e = ExecutorError(f"`{module_name}` does not found in builtin modules; "
                              f"Check this: {', '.join(self.modules.keys())}")
            e.append(ErrorStackFrame(name))
            raise e

        ModuleClass = self.modules[module_name]

        sub = executor.sub()

        result = ModuleImporter.import_module(ModuleClass, sub)

        if commands:
            result = sub(*commands)

        executor.variables[module_name] = sub.variables.get_scope(module_name)

        return result

    def _do_import(self, path_: LexerResultT, commands: LexerResultT = None, *, executor):
        path = executor(path_)
        try:
            source = FileSource(path)
        except FileNotFoundError:
            raise ExecutorError(f"Module does not exist: {path}")
        sub = executor.sub()

        sub.run(source)

        scope = sub.variables.get_scope(path)

        if commands:
            sub(*commands)

        return scope

    def _do_import_inline(self, path_: LexerResultT, executor):
        path = executor(path_)
        try:
            source = FileSource(path)
        except FileNotFoundError:
            raise ExecutorError(f"Module does not exist: {path}")

        result = executor.run(source)

        return result
