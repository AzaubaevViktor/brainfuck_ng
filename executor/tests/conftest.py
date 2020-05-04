import pytest

from executor import Executor
from executor.builtin import ModuleImporter

_importer = ModuleImporter()


@pytest.fixture(scope='function')
def executor():
    # TODO: One scope please
    executor = Executor(_importer.scope_with_import)

    executor.run('(import:scan executor/builtin/_test)')
    executor.run('(import:builtin _test)')
    executor.run('(print "Ready to test boooy?")')

    return executor
