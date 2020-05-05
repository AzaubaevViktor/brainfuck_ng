import pytest

from executor import Executor
from executor.builtin import ModuleImporter


@pytest.fixture(scope='function')
def executor():
    # TODO: One scope please
    executor = Executor(ModuleImporter.scope_with_import())

    from executor.tests._test_module import TestModule
    # executor.run('(import:scan executor/tests/_test_module.py)')
    executor.run('(import:builtin:inline _test)')
    executor.run('(print "Ready to test boooy?")')

    return executor
