# BrainFuck NextGen

Высокоуровневый лиспоподбный язык, зачем-то транслирующийся в brainfuck

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
