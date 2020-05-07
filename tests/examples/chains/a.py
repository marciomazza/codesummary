p = 1
p = 2
p = "."
p = p + "*"

s = "a"
s = "aa"
s = "aaa"
s = "aaaa"
s += f"{s}bb"
import re

m = re.match(p, s)

____________________

import re

p = "."
p = p + "*"

s = "aaaa"
s += f"{s}bb"

m = re.match(p, s)
