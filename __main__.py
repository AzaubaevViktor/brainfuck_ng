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
from executor.builtin._base_builtin import BaseBuiltin

from lexer import do_lex


variables = {
    'about': "REPL v1",
    'version': 1,
    '@': globals(),
    'debug': True,
}

_importer = ModuleImporter()

executor = Executor(_importer.scope_with_import, **variables)

_init = """
(import:builtin builtin)
(print "Hello from LolLisp interpreter!")
(print "Version:" version)
(print "Little magic here...")

(= @exec (item @ "executor"))
(= @vars (. (item @ "executor") variables))

(print "Now you can use `@exec` and `@vars`")
(print "Enjoy!")
(print "To disable debug output use:")
(print "(= debug False)")
"""

executor(*do_lex(_init))

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
        except:
            print_exc()
        finally:
            print()

