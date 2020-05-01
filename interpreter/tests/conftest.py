from bytecode import ByteCode
from interpreter import Mem

_debug_bc = {
    ByteCode.MEM: '+',
    ByteCode.POS: ">",
    ByteCode.PRINT: ".",
    ByteCode.READ: ",",
    ByteCode.CYCLE_START: "[",
    ByteCode.CYCLE_STOP: "]"
}


def _print_items(items, current, fmt='{{{}}}', fmt_item='{}'):
    for index_, item_ in enumerate(items):
        item = fmt_item.format(item_)

        if index_ - 1 == current:
            s = f" {item}"
        elif index_ + 1 == current:
            s = f"{item} "
        elif index_ == current:
            s = fmt.format(item)
        else:
            s = f" {item} "

        print(s, end='')
    print()


def debug_interpreter_step(step: int, code: ByteCode, CP: int, mem: Mem, MP: int, out: str):
    print(">>", step, f"CP: {CP}; MP: {MP}")

    _print_items(code.items, CP, fmt_item="{0[0]}:{0[1]}")
    _print_items(mem.data, MP, fmt_item="{:3}")
    print(out)