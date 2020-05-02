# A |
class A:
    ...


# A A.m | B x
class A(B):
    def m():
        print(x)


# A A.x A.B A.B.C A.B.C.y |
class A:
    x = 1

    class B:
        class C:
            y = x + 1


# A A.x A.z | B C D y
class A(B, C, D):
    x = y + 1
    z = (x, x)


# decorators
# A A.f | b c d
@b
@c(d)
class A:
    @property
    def f(self):
        ...
