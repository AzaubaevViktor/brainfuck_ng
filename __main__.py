"""
TODO:

Install wrapper for packages
Run file
Add extensions (modules) dir
Interactive mode

"""
import sys
from traceback import print_exc

from executor import Executor, ExecutorError
from executor.builtin import ModuleImporter
from modules.builtin import BaseBuiltin

from lexer import do_lex, BaseSource

variables = {
    'version': 2,
    '@': globals(),
    'debug': True,
}


executor = Executor(ModuleImporter.scope_with_import(), **variables)

try:
    executor(*do_lex('(import:inline "modules/repl.lsp")'))
except ExecutorError as e:
    print(e.pretty())
    raise

if __name__ == '__main__':
    while True:
        sys.stdout.flush()
        sys.stderr.flush()

        s = input("~~> ")
        try:
            print(executor.run(s))
        except ExecutorError as e:
            print(e.pretty())
        except SystemExit:
            raise
        except:
            print_exc()
        finally:
            print()

