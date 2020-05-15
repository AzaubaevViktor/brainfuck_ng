#!/usr/bin/env python3

"""
TODO:

Install wrapper for packages
Run file
Add extensions (modules) dir
Interactive mode

"""
import sys
from time import time
from traceback import print_exc, format_exc
from typing import Iterable

import click as click
import readchar as readchar

from executor import Executor, ExecutorError
from executor.builtin import ModuleImporter

from lexer import do_lex, BaseSource

variables = {
    'version': 2,
    '@': globals(),
    'debug': False,
}


from modules.builtin import BaseBuiltin  # Importing Base Builtin values
print(f"Builtin here: {BaseBuiltin}")
executor = Executor(ModuleImporter.scope_with_import(), **variables)

variables = executor.variables

try:
    executor(*do_lex('(import:inline "modules/repl.lsp")'))
except ExecutorError as e:
    print(e.pretty())
    raise


import curses


class StdInSource(BaseSource):
    def __init__(self):

        # ----- INIT -----
        self.stdscr = curses.initscr()
        curses.cbreak()
        curses.noecho()
        # self.stdscr.keypad(1)

        # # ----- PRINT -----
        # text = "Hello world"
        # self.stdscr.addstr(1, 0, text + "\n")
        # self.stdscr.refresh()

        # # ----- MAIN LOOP ------
        # while 1:
        #     c = stdscr.getch()
        #     if c == ord('q'):
        #         break
        #     if c == 8 or c == 127 or c == curses.KEY_BACKSPACE:
        #         stdscr.addstr("\b \b")
        #     else:
        #         stdscr.addch(c)

        # ----- RESET TERMINAL -----
    def shutdown(self):
        import curses

        curses.echo()
        curses.nocbreak()
        # self.stdscr.keypad(1)
        curses.endwin()

    def __iter__(self) -> Iterable[str]:
        s = ""
        while True:
            raw_data = click.getchar()

            if len(raw_data) > 1:
                self.print()
                self.print(f"Command: {', '.join(map(str, map(ord, raw_data)))}")
                break

            char = ord(raw_data)

            if variables['debug']:
                self.print(f"Key: {char}: {chr(char)} ")

            if char == 13:
                break

            if char == 8 or char == 127 or char == curses.KEY_BACKSPACE:
                if s:
                    self.print("\b \b", end='')
                    s = s[:-1]
            else:
                self.print(chr(char), end='')
                s += chr(char)

        self.print()

        # TODO: Control input lines
        # TODO: Use Lexer for more informative output
        # TODO: Colorize
        # TODO: Smart enter
        yield from s

    def __eq__(self, other: "BaseSource"):
        return True

    def print(self, *args, end="\n\r", **kwargs):
        s = " ".join(map(str, args))
        s += " ".join(f"{k}={v}" for k, v in kwargs.items())
        s += str(end)

        sys.stdout.write(s)
        sys.stdout.flush()


if __name__ == '__main__':
    source = StdInSource()

    print = source.print

    while True:
        print("╰~~>", end=' ')

        try:
            print(executor.run(source))
        except ExecutorError as e:
            print(e.pretty())
        except (SystemExit, KeyboardInterrupt):
            source.shutdown()
            raise
        except:
            print(format_exc())
        finally:
            time_ = time()
            print(f"╭ {time_:.0f} {'DEBUG' if variables['debug'] else ''}")



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

