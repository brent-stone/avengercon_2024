## What is Celery

Celery is a pure-Python implementation of what Dask calls _bags_ or Prefect calls
_tasks_ and _flows_. It is designed to coordinate data among machines and processes
[using brokers](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html#brokers)
like Redis, RabbitMQ, and Amazon SQS. It can also store the results of code directly to
a [backend you're probably already using](https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-result-backend-settings)
such as AWS S3, Azure Blob, Elasticsearch, various databases, and plain files.

It's a relatively simple framework compared to Dask or Apache Beam since it only
requires Python to work. Like Dask, it has a scheduler helping work get passed to workers
that actually run the code. Like Prefect, it's generally _embedded_ into your own
codebase using the `#!python @task` decorator above your functions.

## What is Flower

_right click and "open in new tab"_

[Celery :simple-celery:](http://celery.localhost:57073/){ .md-button .md-button--primary}

Flower is a companion project for Celery to provide a GUI for the scheduler similar to
what we saw with Dask and Prefect (albeit not as pretty).

## Getting started with Celery: the Canvas API

Celery calls its main workflow API [canvas](https://docs.celeryq.dev/en/stable/userguide/canvas.html).

The [use guide](https://docs.celeryq.dev/en/stable/userguide/index.html) does a good job
kick-starting understanding but here is a quick summary of the ideas:

1. The [Celery App](https://docs.celeryq.dev/en/stable/userguide/application.html) is
a long-running process that essentially starts the scheduler server. Here we'll call
this run time Python object `app`.

2. Individual Python functions are made into [Celery Tasks](https://docs.celeryq.dev/en/stable/userguide/calling.html#example)
by registering them with a decorator above the function declaration like
`#!python @app.task`

3. [Chains](https://docs.celeryq.dev/en/stable/userguide/canvas.html#chains) are when
there's a sequential series of steps you'd like placed together. These steps can fork &
recombine, represent a parallel computation (via Groups), an individual Task, etc. Each
part of the chain can get all, some, or none of the output created by previous steps.

4. [Groups](https://docs.celeryq.dev/en/stable/userguide/canvas.html#groups) are for
when there's multiple Tasks, Chains, other groups, etc. that aren't dependent on each
other that you'd like to execute in parallel.

**That's it!**. There's more to the API but the vast majority of working with Celery is
arranging Tasks into a [_Directed Acyclic Graph (DAG)_](https://en.wikipedia.org/wiki/Directed_acyclic_graph)
via Chains and Groups.

## Tips for working with the Celery

1. Check out the [Tips and Best Practices](https://docs.celeryq.dev/en/stable/userguide/tasks.html#tips-and-best-practices)
section of the documentation.

2. Celery Tasks can't call Celery Tasks. They can't be "nested"

3. Default behavior is for Celery tasks to have [preset timeouts](https://docs.celeryq.dev/en/stable/userguide/workers.html#time-limits)
It's worth taking time to understand how to adjust timeouts for tasks.

4. When using Chains, if a previous Task produces an output then the following Task will
be passed that as in input. This isn't a bad thing but makes it tricky to craft your
function declarations without doing some guess-and-check to determine exactly what gets
passed between functions.

5. Think of inter-task communication like a webpage calling back to a server. When using
the [default JSON serializer](https://docs.celeryq.dev/en/stable/userguide/calling.html#serializers),
it's important to realize that integers like 1 will arrive as the string "1". Also,
Python objects like a Pandas Dataframe need to be converted to something that can be
serialized into a string value in JSON.

6. Unlike Dask or Apache Beam that help minimize the possibility of race conditions,
be very careful when using Celery to work with a database or other "source of truth"
shared by Tasks executing in parallel via a Group.

7. Make sure the Celery Application "sees" your tasks. The first step is to add anywhere
you've declared tasks with the `#!python @app.task` decorated to the App's `include`

!!! info "Including tasks with the Celery App"
    ```python title="avengercon.celery.tasks.py"

    from avengercon.celery import celery_server

    @celery_server.task(name="tasks.hello_avengercon", ignore_result=False)
    def hello_avengercon() -> str:
        return "Hello, AvengerCon! <3 Celery"
    ```

    ```python title="avengercon.celery.config.py"
    include = [
        "avengercon.celery.tasks",
    ]
    ```

    ```python title="celery.py"
    from avengercon.celery import config
    from celery import Celery

    celery_server: Celery = Celery(main="avengercon")
    celery_server.config_from_object(obj=config, silent=False, force=True)
    ```

    When starting the Celery App, you'll see the tasks listed in the logs
    ``` terminal title="Terminal Logs" hl_lines="16-17"
    avengercon-celery              |  -------------- celery@1f7940b050a2 v5.3.6 (emerald-rush)
    avengercon-celery              | --- ***** -----
    avengercon-celery              | -- ******* ---- Linux-6.5.0-21-generic-x86_64-with-glibc2.36 2024-02-27 15:39:34
    avengercon-celery              | - *** --- * ---
    avengercon-celery              | - ** ---------- [config]
    avengercon-celery              | - ** ---------- .> app:         avengercon:0x7f391a996250
    avengercon-celery              | - ** ---------- .> transport:   redis://:**@redis:6379/0
    avengercon-celery              | - ** ---------- .> results:     redis://:**@redis:6379/0
    avengercon-celery              | - *** --- * --- .> concurrency: 24 (prefork)
    avengercon-celery              | -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
    avengercon-celery              | --- ***** -----
    avengercon-celery              |  -------------- [queues]
    avengercon-celery              |                 .> celery           exchange=celery(direct) key=celery
    avengercon-celery              |
    avengercon-celery              |
    avengercon-celery              | [tasks]
    avengercon-celery              |   . tasks.hello_avengercon
    avengercon-celery              |
    avengercon-celery              | [2024-02-27 15:39:35,400: INFO/MainProcess] Connected to redis://:**@redis:6379/0
    avengercon-celery              | [2024-02-27 15:39:35,401: INFO/MainProcess] mingle: searching for neighbors
    avengercon-celery              | [2024-02-27 15:39:36,405: INFO/MainProcess] mingle: all alone
    ```
