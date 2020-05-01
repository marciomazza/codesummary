# a.b | a
a.b = 2


# a.b.c | a a.b
a.b.c = 1


# f | a
def f():
    a.b = 2
    x = a.b
