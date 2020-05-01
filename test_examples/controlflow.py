# | a
if a == 1:
    ...


# a | b
for a in b:
    ...


# | a
while a:
    ...


# a b | x y
with x as a, y as b:
    ...


# name "e" is local to the exception block
# |
try:
    ...
except Exception as e:
    ...
