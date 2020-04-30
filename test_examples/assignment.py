# a |
a = 1


# a | b
a = b


# a b | x y
a, b = x, y


# a | f x y
a = f(x + y)


# del alters the variable. for our use that's a "store"
# a |
del a


# dict assignment
# a | a
a[1] = 2


# x | a
x = a[1]


# del in dict
# a | a
del a[1]
