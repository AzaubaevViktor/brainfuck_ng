(import:builtin:inline builtin)

(print "Hello from LolLisp REPL interpreter!")
(print "Version:" version)

(print "Little magic happens here...")

(= @exec (item @ "executor"))
(= @vars (. @exec variables))

(print "Now you can use: `@exec` and `@vars`")
(print)
(print "To enable debug output use:")
(print "(= debug True)")

#(= == (op eq))

(defn help [name] (
    (if ((op eq) name "help")
        (print "✅ You can do it!")
        (print "And you can do:")
        (print "  : (exit 0)")
        (print "  : (+ 1 1)")
        (print "  : (help \"@vars\"")
        (print "  : (help \"@exec\"")
    )

#    (if (== name "@vars")
#        (print "Словарь переменных, который использует @exec")
#        (print)
#        (print "В словаре есть методы, их можно запускать так:"
#        (print "  : (* 100 200)")
#        (print "  : (+ 1 (/ 1 2))")
#        (print "  : (== (+ 1 (/ 1 2)) 1.5)")
#        (print)
#        (print "Добавить значение в @vars:")
#        (print "  : (= var_name (+ 1 1))")
#        (print)
#        (print "help \"defn\"")
#    )
#
#    (if (== name "@exec")
#        (print "Нигде не используется")
#    )

))

(print "To show help use: (help \"help\")")
(print)
(print "Enjoy!")


