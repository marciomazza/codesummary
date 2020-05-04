# a.b | a
a.b = 2


# a.b.c | a a.b
a.b.c = 1


# f | a
def f():
    a.b = 2
    x = a.b


# an augmented assignment also depends on the variable
# a.b.c | a a.b a.b.c
a.b.c += 1


# a call stops a subsequent attribute load
# | g
g().a


# | g
g().a.b


# a call stops a subsequent attribute store
# | g
g().a = 1


# | g
g().a.b = 1
