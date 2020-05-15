#!/usr/bin/env python3

"""
TODO:

Install wrapper for packages
Run file
Add extensions (modules) dir
Interactive mode

"""
import sys
from traceback import print_exc
from typing import Iterable

import click as click
import readchar as readchar

from executor import Executor, ExecutorError
from executor.builtin import ModuleImporter

from lexer import do_lex, BaseSource

variables = {
    'version': 2,
    '@': globals(),
    'debug': True,
}


from modules.builtin import BaseBuiltin  # Importing Base Builtin values
print(f"Builtin here: {BaseBuiltin}")
executor = Executor(ModuleImporter.scope_with_import(), **variables)

try:
    executor(*do_lex('(import:inline "modules/repl.lsp")'))
except ExecutorError as e:
    print(e.pretty())
    raise


class StdInSource(BaseSource):
    def __iter__(self) -> Iterable[str]:
        s = ""

        while True:
            char = click.getchar()
            if char == "\n" or char == "\r":
                break

            s += char
            sys.stdout.write(char)
            sys.stdout.flush()

        sys.stdin.flush()

        print()

        # TODO: Control input lines
        # TODO: Use Lexer for more informative output
        # TODO: Colorize
        # TODO: Smart enter
        yield from s

    def __eq__(self, other: "BaseSource"):
        return True


if __name__ == '__main__':
    source = StdInSource()

    while True:
        sys.stderr.flush()
        sys.stdout.write("~~> ")
        sys.stdout.flush()

        try:
            print(executor.run(source))
        except ExecutorError as e:
            print(e.pretty())
        except (SystemExit, KeyboardInterrupt):
            raise
        except:
            print_exc()
        finally:
            print()


def old_main():
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

