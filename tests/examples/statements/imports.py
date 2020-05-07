# a |
import a


# a |
import aaa as a


# b |
from a import b


# b |
from x import bb as b


# (try block to avoid black changing the import)
# a b c |
try:
    import aa as a, b, ccc as c
finally:
    ...
