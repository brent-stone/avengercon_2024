## What is Dask?

[This article](https://www.nvidia.com/en-us/glossary/dask/) by NVIDIA has decent
infographics and explanations on what Dask is. The VERY summarized explanation is it's a
library that combines [Tornado](https://www.tornadoweb.org/en/stable/) and Pandas so
that an arbitrary number of Python interpreters and Pandas DataFrames can be used as if
they were a single interpreter and DataFrame.

The [Journey of a Task](https://distributed.dask.org/en/latest/journey.html) explanation
by the Dask authors provides a nice intro to how the framework operates.

## What is Coiled and Prefect?
Dask fits into a growing segment of the data/tech industry where Free and Open Source
Software (FOSS) is provided with fully-managed and extended offerings made available by
the primary contributors to make an income.

Two of the more prominent companies aligned with Dask are [Coiled.io](https://www.coiled.io/)
and [Prefect](https://www.prefect.io/).


## Dask created hands-on crash course

[Jupyter Notebook :simple-jupyter:](http://notebook.localhost:57073/){ .md-button .md-button--primary}

Transition to the official crash-course running on your computer to get comfortable with
the framework.

## Preparing for using Dask in your own projects

Since we've already seen some basics of using Dask in the Jupyter notebooks, let's
transition to a couple of tasks using Prefect.

### Open the Prefect User Interface

Right-click and "open in new tab"

[Prefect :simple-prefect:](http://prefect.localhost:57073/dashboard){ .md-button .md-button--primary}

### Integrating Prefect with AWS S3/MinIO

In your IDE with your virtual environment activated ([as described earlier](1_hello_workshop.md)),
try making and running a new python script in the `avengercon_2024` directory.

``` py title="testing.py"
from avengercon.prefect.flows import hello_prefect_flows
from avengercon.prefect.storage import create_default_prefect_blocks, create_default_prefect_buckets

print(hello_prefect_flows())
create_default_prefect_buckets()
create_default_prefect_blocks()
```

Take a look at the "Blocks" portion of the Prefect UI. You should see `prefect-artifacts`
and `prefect-flows` as registered S3-like buckets. Clicking the link on either will
show instructions on how to use these buckets in the future to cache both the files your
team is working on and the code you're using to do so. This may be particularly helpful
when your operators may want to trigger a pre-defined series of steps for new data by
triggering a [deployment](https://docs.prefect.io/latest/concepts/deployments/) that
uses a [flow](https://docs.prefect.io/latest/concepts/flows/) the dev team stored in a
block.
