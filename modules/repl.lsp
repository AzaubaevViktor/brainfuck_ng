(import:builtin:inline builtin)

(print "Hello from LolLisp REPL interpreter!")
(print "Version:" version)

(print "Little magic happens here...")

(= @exec (item @repl "executor"))
(= @vars (. @exec variables))

(print "Now you can use: `@exec` and `@vars`")
(print)
(print "To enable debug output use:")
(print "(= debug True)")

(= == (op eq))

(defn help [name] (
    (if ((op eq) name "help")
        (print "✅ You can do it!")
        (print "And you can do:")
        (print "  : (exit 0)")
        (print "  : (+ 1 1)")
    )
))

(print "To show help use: (help \"help\")")
(print)
(print "Enjoy!")


