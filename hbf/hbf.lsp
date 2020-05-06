(import:builtin:inline hbf)

(@defmacrocommand @go [addr] (
    (@_go addr)
    (@super:inline)
    (@_back addr)
))

(@defmacrocommand @back [addr] (
    (@_back addr)
    (@super:inline)
    (@_go addr)
))

(@defmacro @inc [addr value] (
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
        (@_cycle (
            (@back addr (
                (@super:inline)
            ))
        ))
    ))
))

(@defmacro @zero [addr] (
    (@go addr (
        (@_cycle (
            (@_plus -1)
        ))
    ))
))

(@defmacro @set [addr value] (
    (@zero addr)
    (@inc addr value)
))
