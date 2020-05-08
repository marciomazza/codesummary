# codesummary

***Transitive dependency resolution for python statements.***

Given a list of python statements, *summarize* them to the minimal sub-list of statements necessary to reach the same result of the *last statement*.

To solve this we transitively resolve the dependencies of the *last statement*, filtering out the unnecessary ones.

For example, given this list of statements:

```python
z = 'unnecessary'
p = "another unnecessary one"
p = ".*"

s = "also not needed"
s = "aaa"
s += f"{s}bb"

import re

m = re.match(p, s)
```

its *summary* is:

```python
import re

p = ".*"
s = "aaa"
s += f"{s}bb"
m = re.match(p, s)
```

### Function side-effects

Although trying to minimize the list of dependencies, the `summarize` method has *limited access* to function implementations.

So, to err on the safe side, we assume that
***function calls may alter they arguments***.

For example, whenever we see a call statement `function(arg)` preceding a plain `arg` statement, we take such call be a dependency of this last statement.  That means this list:

```python
arg = 2
print(function(arg))
arg
```
is its own summary and *not* simply
```python
arg = 2
arg
```
To sum it up, the *summary* is not necessarily minimal, but minimal assuming function calls alter their arguments.

## Installation

```bash
pip install codesummary
```

## Usage

```python
In [1]: text = '''p = 2
   ...: p = ".*"
   ...: s = "aa"
   ...: s = "aaa"
   ...: s += f"{s}bb"
   ...: import re
   ...: m = re.match(p, s)'''

In [2]: statements = text.splitlines()

In [3]: from codesummary import summarize
   ...:
   ...: print('\n'.join(summarize(statements)))

import re
p = ".*"
s = "aaa"
s += f"{s}bb"
m = re.match(p, s)
```
