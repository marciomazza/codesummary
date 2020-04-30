# expression in parameter
# f | x
def f(a, b=x):
    ...


# expression in parameter
# f | g x
def f(a, b=g(x)):
    ...


# names bound to parameter (bound in lexical scope) are ignored
# f | x
def f(a, b):
    c = a + x


# no repetitions
# f | x y
def f():
    print(x, y)
    print(x)
    y = x + y


# f | g
def f(a, b):
    c = g(a, b)


# builtins are ignored
# f |
def f():
    print(len([1, 2, 3]))


# f | re
def f(a):
    re.match(".", a)


# local scope variables are ignored
# f | a b
def f():
    x = a + b
    print(x)


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
        print(a, b, c, x, y, z)


# function referenced after defined
# f | h
def f():
    def g():
        ...

    g()
    h()
