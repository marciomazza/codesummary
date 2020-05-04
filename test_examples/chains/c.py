a = 1
a = int(2.3)


def f():
    yield a


def f():
    return float(a)


b = []
b = [f(), 0, 0]
b.append(12)
print(b[1])
____________________

a = int(2.3)


def f():
    return float(a)


b = [f(), 0, 0]
b.append(12)
print(b[1])
