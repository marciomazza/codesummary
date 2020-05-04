# f potentially alters a, so we store it
# a | f a
f(a)


# ignore the argument that is not a simple name
# a b | f a b c d
f(a, b, c + d)


# function call involving attributes
# a.b.c | f a a.b a.b.c
f(a.b.c)


# a method call potentially alters the object, so we store it
# a | a a.f
a.f()


# a b | a a.f b
a.f(b)


# method call involving attributes
# a.b | a a.b a.b.f
a.b.f()


# a.b.c | a a.b a.b.c a.b.c.f
a.b.c.f()


# a call stops a subsequent attribute store
# a | f a
f().g(x=a)


# a | f a
f()(a)


# a b | a a.g b
a.g()(b)
