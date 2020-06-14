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

from lexer import do_lex, BaseSource, LexerError

repl_vars = {
}

variables = {
    'version': 3,
    'debug': False,
    '@repl': repl_vars,
}


from modules.builtin import BaseBuiltin  # Importing Base Builtin values
print(f"Builtin here: {BaseBuiltin}")
repl_vars['executor'] = executor = Executor(ModuleImporter.scope_with_import(), **variables)

repl_vars['variables'] = variables = executor.variables


try:
    executor(*do_lex('(import:inline "modules/repl.lsp")'))
except ExecutorError as e:
    print(e.pretty())
    raise


import curses


class StdInSource(BaseSource):
    def __init__(self):
        self.debug = False

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

    def _new_chars(self):
        raw_data = click.getchar()

        if len(raw_data) == 1:
            yield raw_data

        if len(raw_data) > 1:
            if self.debug:
                self.print()
                self.print(f"Command: {', '.join(map(str, map(ord, raw_data)))}")

            # UP, DOWN, LEFT, RIGHT keys
            if len(raw_data == 3) and raw_data[0] == 27 and raw_data[1] == 91:
                if self.debug:
                    # TODO: Implement history
                    self.print("Not implemented yet")
                return

            yield from raw_data

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

            if char == 13:  # Enter key
                try:
                    do_lex(s)
                    break
                except LexerError as e:
                    # TODO: Fix Multiline inputs, f.e. defn
                    if e.ns_stack:
                        pos = e.ns_stack[-1].pos + 1
                        self.print(f"\n{'':<5}" + ("·" * (pos - 1)), end=' ')
                        s += "\n" + " " * pos
                    continue

            if char == 8 or char == 127 or char == curses.KEY_BACKSPACE:
                if s:
                    self.print("\b \b", end='')
                    s = s[:-1]
            else:
                self.print(chr(char), end='')
                s += chr(char)


            if self.debug:
                self.print(s)

        self.print()

        if self.debug:
            self.print("Command received")

        # TODO: Control input lines
        # TODO: Use Lexer for more informative output
        # TODO: Colorize
        # TODO: Smart enter
        yield from s

    def __eq__(self, other: "BaseSource"):
        return True

    def print(self, *args, end="\n", **kwargs):
        s = " ".join(map(str, args))
        s += " ".join(f"{k}={v}" for k, v in kwargs.items())
        s += str(end)

        s = s.replace("\n", "\n\r")

        sys.stdout.write(s)
        sys.stdout.flush()

    def _print(self, *objs: 'LexerResultT', executor):
        self.print(*map(executor, objs))


if __name__ == '__main__':
    repl_vars['lexer'] = source = StdInSource()

    variables['print'] = source._print

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
            print(format_exc().replace("\n", "\n\r"))
        finally:
            time_ = time()
            print(f"╭ {time_:.0f} {'DEBUG' if variables['debug'] else ''}")

            source.debug = variables.get('debug', False)


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

