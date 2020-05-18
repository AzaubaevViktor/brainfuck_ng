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

(@defmacro @_move [to from] (
    (@cycle from (
        (@inc from -1)
        (@inc to 1)
    ))
))

(@defmacro @_move2 [to1 to2 from] (
    (@cycle from (
        (@inc from -1)
        (@inc to1 1)
        (@inc to2 1)
    ))
))

(@defmacro @copy [to from] (
    (@zero to)
    (@let res 0)
    (@_move2 res to from)
    (@_move from res)
))

(@defmacro @add [to from] (
    (@let res 0)
    (@copy res from)
    (@cycle res (
        (@inc res -1)
        (@inc to 1)
    ))
))

(@defmacro @if [cond_orig true_branch false_branch] (
    (@let is_false 1)

    (@let cond 0)
    (@copy cond cond_orig)

    (@cycle cond (
        true_branch

        (@set is_false 0)
        (@set cond 0)
    ))

    (@cycle is_false (
        false_branch

        (@set is_false 0)
    ))
))
