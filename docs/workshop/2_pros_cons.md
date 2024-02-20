## Python Parallelization Frameworks

We'll be exploring four different methods for horizontally scaling python in this
workshop:

<div class="grid cards" markdown>
-   :simple-python:{ .lg .middle } __[Python multiprocessing](https://docs.python.org/3/library/multiprocessing.html)__

    ---

    _For when you just need one or two functions to scale. Chances a good that if you
    try to make anything non-trivial, you're going to invest weeks of effort to
    discover you've made a junk version of Dask v0.1 or Celery v0.1. If you don't know
    what a [lamport clock](https://martinfowler.com/articles/patterns-of-distributed-systems/lamport-clock.html)
    is, this option probably isn't for you._

    **Pros:**

    :material-checkbox-marked-circle:{ .green } Works "out of the box"

    :material-checkbox-marked-circle:{ .green } Potential for batch & streaming (good luck...)

    **Cons:**

    :octicons-x-circle-24:{ .red }
    Race conditions are on you

    :octicons-x-circle-24:{ .red }
    Memory management is on you

    :octicons-x-circle-24:{ .red }
    Synchronization is on you

    :octicons-x-circle-24:{ .red }
    Inter-process dataflow is on you

-   :simple-dask:{ .lg .middle } __[Dask](https://www.dask.org/)__

    ---

    _Use this if you're already planning on using Pandas. If you aren't using Pandas
and all the benefits of optimized C outside of the GIL it brings, it's worth taking a
pause to double-check you CAN'T use it before using something else._

    **Pros:**

    :material-checkbox-marked-circle:{ .green }
    Nearly 1-for-1 API parity with standard Pandas

    :material-checkbox-marked-circle:{ .green }
    Effortless scaling for Dataframe-based workflows

    :material-checkbox-marked-circle:{ .green }
    Support for non-Dataframe tasks

    :material-checkbox-marked-circle:{ .green }
    Painless infrastructure integration

    :material-checkbox-marked-circle:{ .green }
    1st class support for GPUs (via [RAPIDS](https://rapids.ai/))

    **Cons:**

    :octicons-x-circle-24:{ .red }
    Centered around Pandas (columnar data)

    :octicons-x-circle-24:{ .red }
    Complex workflows aren't a strong suit

    :octicons-x-circle-24:{ .red }
    Getting custom code & dependencies onto workers is a learning curve

    :octicons-x-circle-24:{ .red }
    While streaming may be theoretically possible, it's built for batch workflows

-   :simple-celery:{ .lg .middle } __[Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)__

    ---

    _The Python parallelization swiss-army knife. This can do whatever you're trying to do._

    **Pros:**

    :material-checkbox-marked-circle:{ .green }
    Complex workflows are a specialty

    :material-checkbox-marked-circle:{ .green }
    Integrating your project code & dependencies is the default

    :material-checkbox-marked-circle:{ .green }
    Quirky but relatively painless infrastructure

    :material-checkbox-marked-circle:{ .green }
    Probably supports where you store your data

    **Cons:**

    :octicons-x-circle-24:{ .red }
    Canvas (workflow) API has a learning curve

    :octicons-x-circle-24:{ .red }
    Poor support for arbitrarily long tasks

    :octicons-x-circle-24:{ .red }
    Inter-process JSON messages can be difficult to predict

    :octicons-x-circle-24:{ .red }
    :octicons-moon-16: Flower doesn't have a dark mode

-   :simple-apache:{ .lg .middle } __[Apache Beam](https://beam.apache.org/)__

    ---

    _This is the endgame :muscle: If you're truly starting to scale but don't want to
    ditch Python, then your journey will probably lead here._

    **Pros:**

    :material-checkbox-marked-circle:{ .green }
    Forces effective map-shuffle-reduce patterns

    :material-checkbox-marked-circle:{ .green }
    Potentially fastest (with :simple-apacheflink: Apache Flink) and scales [harder than
    Chuck Norris can kick](https://youtu.be/E6UTz_Doic8?si=pGZkyRAQVMxi-Ymh&t=22)

    :material-checkbox-marked-circle:{ .green }
    1st class support for streaming dataflows and all the complexity that goes along with
    that (windowing, late arrivals, only once, at least once, etc.)

    :material-checkbox-marked-circle:{ .green }
    Leverage existing infrax (:simple-googlecloud: GCP, :simple-apachespark: Spark, etc.)

    :material-checkbox-marked-circle:{ .green }
    Create effective Spark/Flink jobs with Python


    **Cons:**

    :octicons-x-circle-24:{ .red }
    Just an abstraction layer (less the dev-only Direct Runner)

    :octicons-x-circle-24:{ .red }
    Complex infrax setup for self-hosted prod deployment

    :octicons-x-circle-24:{ .red }
    Semi-linked to GCP's DataFlow implementation

    :octicons-x-circle-24:{ .red }
    Chained dependencies cause projects to be stuck with months old libraries

    :octicons-x-circle-24:{ .red }
    Semi-locked in options for sources and sinks

</div>


## When are all of these options a bad idea?

Spending weeks learning a new language is likely going to be slower than writing
something in a language you already know today (CPython) and running it. That said,
CPython is very upfront about its inability to use threading. Python 3.12+ is beginning
the slow process of overcoming the Global Interpreter Lock (GIL) inability to support
multiple threads. Details are in [PEP 703](https://peps.python.org/pep-0703/).

Until the GIL supports threads and the Python ecosystem (SciPy, Dask, FastAPI, etc.)
adapts to the change, the best case scenario with Python is multiprocessing using
orders of magnitude more memory, layers of complexity, and slightly more time to
accomplish a task compared to what compiled languages with threading can accomplish with
basic functions.

## Vertically scaling "Python"

While this workshop is focused on **horizontally** scaling Python, it's worth making
some honorable mentions for vertically scaling individual Python interpreters to be
more performant. The theme here is: speed up Python by minimizing the use of Python.

<div class="grid cards" markdown>

-   :material-language-c:{ .lg .middle } __Wrap C & C++ with Python__

    ---

    This likely isn't new information, but directly [extending Python with C or C++](https://docs.python.org/3/extending/extending.html)
    is how Numpy, Pandas, and much of the CPython standard library is made.

-   :material-language-c:{ .lg .middle } __Compile and Cache Python__

    ---

    [py_compile](https://docs.python.org/3/library/py_compile.html) and
    [functools.lru_cache](https://docs.python.org/3/library/functools.html)
    are "out of the box" and relatively painless ways to speed up your critical path.

    Chances are pretty good that the Python interpreter is already compiling your code
    to `.pyc` files.

-   :simple-numba:{ .lg .middle } __[Numba](https://numba.pydata.org/)__

    ---

    **Step 1**. Put `#!python @njit` above `#!python def my_function()`

    **Step 2**. Magic

-   :simple-taichilang:{ .lg .middle } __Embedding [Taichi](https://www.taichi-lang.org/) into Python__

    ---

    You can install it with pip, write it in your `.py` files, and it looks like Python.
    BUT... you're not _really_ using Python anymore. Similar situation as Numba:

    **Step 1**: Hop on a magic carpet with `#!python ti.init(arch=ti.gpu)`

    **Step 2**: Put `#!python @ti.func` or `#!python @ti.kernel` above your function.

    **Step 3**: Magic

</div>

[![Benchmarks](2_images/benchmark_numba_cuda_taichi.png)](https://docs.taichi-lang.org/blog/taichi-compared-to-cub-cupy-numba)