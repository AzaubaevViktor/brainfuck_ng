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

from lexer import do_lex


variables = {
    'version': 2,
    '@': globals(),
    'debug': True,
}


executor = Executor(ModuleImporter.scope_with_import(), **variables)

try:
    executor(*do_lex('(import "modules/repl.lsp")'))
except ExecutorError as e:
    print(e.pretty())
    raise

if __name__ == '__main__':
    while True:
        sys.stdout.flush()
        sys.stderr.flush()

        s = input("~~> ")
        try:
            lex_result = do_lex(s)
            if executor.variables.get('debug', True):
                print(lex_result)
            print(executor(*lex_result))
        except ExecutorError as e:
            print(e.pretty())
        except SystemExit:
            raise
        except:
            print_exc()
        finally:
            print()

