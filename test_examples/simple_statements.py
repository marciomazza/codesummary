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


# a |
a += 1


# a | b
a &= b


# a | b
(a := b)


# | a
await a


# a global var declaration creates a dependency (load)
# | a b
global a, b


# a nonlocal can only be valid code when already pointing to a variable
# in some local scope. So a "nonlocal" does not create a dependency (load)
# |
nonlocal a, b
