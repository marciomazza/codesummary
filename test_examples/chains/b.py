# f | a
def f(x):
    return a


# g | a
def g(y):
    yield a, b


a = 1
c = " "
a += 1
b = None
b = a + 2
c = f(b)

____________________

# f | a
def f(x):
    return a


a = 1
a += 1
b = a + 2
c = f(b)
