# Factory - Python Multithreading ELI5'd

Factory provides a convenient way to do 'n' jobs using a worker function in 'm' threads in Python.

## Getting Started

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

Here's another example of usage inside a class:

```python
from factory import Factory

class FancyThing:
    def __init__(self):
        self.x = 12

    def fancy_work(self, fanciness):
        return fanciness*(fanciness+self.x)

    def mass_fancy(self, swag=10):
        f = Factory(worker=self.fancy_work, num_workers=swag/2)
        return f.work(range(swag*2))

print FancyThing().mass_fancy()
```

Factory can also work for you asynchronously:

```python
from factory import Factory

def myworker(x):
    return x*x*x

source = range(1,51)
f = Factory(worker=myworker, num_workers=5)

for cube in f.work_async(source):
    # print as and when results become available
    print cube

    # optionally break on a condition without having to wait for all workers to finish
    if cube > 3000:
        break

f.close() # it is important to close after async work to prevent zombie threads
```

### But `multiprocessing.Pool` does this

It doesn't. For some reason `multiprocessing.Pool` requires the worker function to be [picklable](http://stackoverflow.com/questions/1816958/), [which is not always the case](https://docs.python.org/2/library/pickle.html#what-can-be-pickled-and-unpickled) for things like the second example above.
