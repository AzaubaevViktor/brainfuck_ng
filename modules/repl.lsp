(import:builtin:inline builtin)

(print "Hello from LolLisp REPL interpreter!")
(print "Version:" version)

(print "Little magic here...")

(= @exec (item @ "executor"))
(= @vars (. @exec variables))

(print "Now you can use `@exec` and `@vars`")
(print "Enjoy!")
(print)
(print "To disable debug output use:")
(print "(= debug False)")
