Factory - Python Multithreading ELI5'd
======================================

Factory provides a convenient way to do 'n' jobs using a worker function in 'm' threads in Python.

Getting Started
---------------

Here's an example of using Factory to squares of first 100 integers using 5 threads.

```python
from factory import Factory

def myworker(x):
    return x*x

source = range(1,101)
f = Factory(worker=myworker, num_workers=5)
squares = f.work(source) # can be any iterable
print squares
```

Note that the results are not guaranteed to be in the same order as the input. You will need to write your own logic to match each result with its input.
