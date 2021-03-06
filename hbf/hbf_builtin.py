from typing import List, Optional

from executor import ExecutorError, Executor
from executor.builtin import BaseModule
from lexer import LexerResultT, Lemma


class Addr:
    def __init__(self, addr: int):
        self.addr = addr

    def __repr__(self):
        return f"<Addr:{self.addr}>"


class HBFError(ExecutorError):
    @staticmethod
    def check_addr(obj: Addr, lemma: Optional[LexerResultT] = None):
        if not isinstance(obj, Addr):
            raise HBFError(f"Must be address, not {type(obj)}", lemma)


class HBFBuiltin(BaseModule):
    NAME = "hbf"

    def __init__(self):
        self.last_address = 0

    def __call__(self, variables):
        return {
            '@_go': self.go,
            '@_back': self.back,
            '@_plus': self.plus,
            '@_print': self.print,
            '@_read': self.read,
            '@_cycle': self.cycle,
            "@let": self.let,
            '@defmacro': self.defmacro,
            '@defmacrocommand': self.defmacro_command,
            '@addr': self.to_addr,
        }

    def to_addr(self, value_: LexerResultT, executor: Executor):
        value = executor(value_)
        return Addr(value)

    # TODO: create this method throught defn:inline
    def let(self, name: Lemma, value: LexerResultT, executor):
        self.last_address += 1

        executor.variables[name.text] = Addr(self.last_address)

        return "".join((self._move(self.last_address),
                        self.plus(value, executor),
                        self._move(-self.last_address)
                        ))

    def _move(self, addr: int):
        if addr < 0:
            return "<" * (-addr)
        return ">" * addr

    def go(self, addr_: LexerResultT, executor):
        addr = executor(addr_)
        HBFError.check_addr(addr, addr_)
        return self._move(addr.addr)

    def back(self, addr_: LexerResultT, executor):
        addr = executor(addr_)
        HBFError.check_addr(addr, addr_)
        return self._move(-addr.addr)

    def plus(self, value_: LexerResultT, executor):
        value = executor(value_)
        if not isinstance(value, int):
            raise HBFError(f"Must be int, not {type(value)}", value_)

        if value < 0:
            return "-" * -value
        return "+" * value

    def print(self, executor):
        return "."

    def read(self, executor):
        return ","

    def cycle(self, commands: LexerResultT, executor):
        result = "["
        for item in commands:
            result += executor(item)
        result += "]"
        return result

    def defmacro(self, name: Lemma, args: List[Lemma], commands: LexerResultT, executor):
        macro_name = name.text

        argument_names = [arg.text for arg in args]

        def macro(*args, executor):
            if len(argument_names) > len(args):
                expected_argument = argument_names[len(args)]
                raise ExecutorError(f"{macro_name}: Expect argument {expected_argument}")

            if len(argument_names) < len(args):
                raise ExecutorError(f"{macro_name}: Too many arguments (expect {len(argument_names)})")

            sub = executor.sub()

            for arg_name, arg in zip(argument_names, args):
                # TODO: Error while argument calculation Exception
                sub.variables[arg_name] = executor(arg)

            result = ""
            for cmd in commands:
                result += sub(cmd)

            return result

        macro.__name__ = macro_name

        executor.variables[macro_name] = macro

        return macro

    def defmacro_command(self, name: Lemma, args: List[Lemma], commands: LexerResultT, executor):
        macro_name = name.text

        argument_names = [arg.text for arg in args]

        def macro_command(*args, executor: Executor):
            commands_wrapped: LexerResultT
            *args, commands_wrapped = args

            if len(argument_names) > len(args):
                expected_argument = argument_names[len(args)]
                raise ExecutorError(f"{macro_name}: Expect argument {expected_argument}")

            if len(argument_names) < len(args):
                raise ExecutorError(f"{macro_name}: Too many arguments (expect {len(argument_names)})")

            clojure_executor = executor

            sub = executor.sub()

            def super_inline(executor: Executor):
                result_inline = ""
                for command in commands_wrapped:
                    result_inline += clojure_executor(command)
                return result_inline

            # if "@super:inline" in sub.variables:
            #     raise ExecutorError(f"⚠️⚠️⚠️ Rewrite @super:inline: {sub.variables['@super:inline']}")
            sub.variables["@super:inline"] = super_inline

            for arg_name, arg in zip(argument_names, args):
                # TODO: Error while argument calculation Exception
                sub.variables[arg_name] = executor(arg)

            result = ""
            for cmd in commands:
                result += sub(cmd)

            return result

        macro_command.__name__ = macro_name

        executor.variables[macro_name] = macro_command

        return macro_command
