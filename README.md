# BrainFuck NextGen

Высокоуровневый лиспоподбный язык, зачем-то транслирующийся в brainfuck

## Описание

```
str -> Lexer -> Executor -> result
```

Лексер разбирает только скобки, леммы и строки (с escaping)  
Исполнитель запускается в базовой области видимости, где можно ставить свои функции
В целом основной цикл интерпретатора работает так:
```python

def my_func(*lemmas, executor):
    pass
    # Do some things with lemmas
    return executor(lemmas[0])(lemmas[1:])

variables = {
    'my_func': my_func,
    'x': 10
}
from executor import Executor
from lexer import do_lex

executor = Executor(variables)

while True:
    inp = input("Omg you run me ~~> ")
    lex_result = do_lex(inp)
    # Some operations with lemmas
    
    result = executor(*lex_result)
    print("Here result:")
    print(result)
```

## REPL
```
~~> ((op add) 12 23)
35

~~> (print "Hello, world!")
Hello, world!

~~> [1 2 3 "four"]
[1, 2, 3, 'four']

~~> [1 2 3 [4 5 6] 7 ]
[1, 2, 3, [4, 5, 6], 7]

~~>[1 2 (op add)]
[1, 2, <function get_operator.<locals>.wrapper_op at 0x102e91a60>]
```

```
~~> (defn + [a b] ( ((op add) a b) ))
<function defn.<locals>.new_func at 0x10440faf0>

~~> (+ 1 2)
3
```

## Трансляция в brainfuck
[Не реализовано]

## Список основных реализаций