(import:builtin:inline hbf)

(@defmacrocommand @go [addr] (
    (@_go addr)
    (@super:inline)
    (@_back addr)
))

(@defmacro @add [addr value] (
    (@go addr (
        (@_plus value)
    ))
))

(@defmacro @print [addr] (
    (@go addr (
        (@_print)
    ))
))


(@defmacro @read [addr] (
    (@go addr (
        (@_print)
    ))
))

(@defmacrocommand @cycle [addr] (
    (@go addr (
        (@cycle (
            (@super:inline)
        ))
    ))
))