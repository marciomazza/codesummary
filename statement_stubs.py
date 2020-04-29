# this file contains test examples of statements and their dependencies


#
a = 1

# b
a = b

# x y
a, b = x, y


# f x y
a = f(x + y)


# x
def f(a, b=x):
    ...


# names bound to parameter (bound in lexical scope) are ignored
# x
def f(a, b):
    c = a + x


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


# a b
def f():
    x = a + b
    print(x)
