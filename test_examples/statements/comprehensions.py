# var in comprehension is local
# |
[i for i in ...]


# | f
[f(i) for i in ...]


# set comprehensions
# |
{i for i in ...}


# | a
{(i, a) for i in ...}


# generator expressions
# | a f
([a, f(i)] for i in ...)


# dict comprehensions
# |
{k: v for k, v in []}


# | a b c
{a: (b, c, k, v) for k, v in []}
