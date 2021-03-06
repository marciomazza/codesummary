# expression in parameter
# f | x
def f(a, b=x):
    ...


# expression in parameter
# f | g h x y
def f(a, b=g(h(x + y))):
    ...


# f | a
def f():
    return a


# f | a
def f():
    yield a


# var and keyword/default args
# f |
def f(p, a, *args, b=1, **kwargs):
    return (p, a, b, args, kwargs)


# positional only args (python 3.8)
# f |
def f(p, /, a):
    return (p, a)


# keyword only args
# f |
def f(a, *, b=1):
    return (a, b)


# names bound to parameter (bound in lexical scope) are ignored
# f | x
def f(a, b):
    c = a + x


# no repetitions
# f | x y
def f():
    yield (x, y)
    yield (x)
    y = x + y


# f | g
def f(a, b):
    c = g(a, b)


# f | re re.match
def f(a):
    re.match(".", a)


# local scope variables are ignored
# f | a b
def f():
    x = a + b
    return x


# free variable outside inner scope
# f | x y
def f():
    def g(x):
        y = 1

    return x, y


# f | a b c
def f(x):
    w = x + a

    def g(y, z):
        return (a, b, c, x, y, z)


# function referenced after defined
# f | h
def f():
    def g():
        ...

    g()
    h()


# decorators
# f | a b
@a
def f():
    return b


# b and c can be altered by a => store them
# b c f | a b c d e y
@a(b, x=c)
@d
@e
def f():
    return y
