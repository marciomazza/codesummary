# this file contains test examples of statements and their dependencies


#
a = 1


# b
a = b


# x y
a, b = x, y


# f x y
a = f(x + y)


# expression in paramenter
# x
def f(a, b=x):
    ...


# names bound to parameter (bound in lexical scope) are ignored
# x
def f(a, b):
    c = a + x


# no repetions
# x y
def f():
    print(x, y)
    print(x)
    y = x + y


# g
def f(a, b):
    c = g(a, b)


# builtins are ignored
#
def f():
    print(len([1, 2, 3]))


# re
def f(a):
    re.match(".", a)


# local scope variables are ignored
# a b
def f():
    x = a + b
    print(x)


# free variable outside inner scope
# x y
def f():
    def g(x):
        y = 1

    return x, y


# a b c
def f(x):
    w = x + a

    def g(y, z):
        print(a, b, c, x, y, z)
