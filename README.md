# Avengercon VIII Workshop <br> Parallel Data Engineering in Python

Repo Status </br>
![Tests](docs/badges/tests.svg)
![Coverage](docs/badges/coverage.svg)
![Interrogate](docs/badges/interrogate_badge.svg)
<!---
Update the CI status to your repo's project name!
https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge
https://docs.gitlab.com/ee/user/project/badges.html#view-the-url-of-pipeline-badges
-->

Tooling </br>
![Python](docs/badges/pyversions.svg)
[![Poetry](docs/badges/poetry.svg)](https://python-poetry.org/)
[![Tox](docs/badges/tox.svg)](https://tox.wiki/)
[![Black](docs/badges/black.svg)](https://black.readthedocs.io/en/stable/)
[![Safety](docs/badges/safety.svg)](https://github.com/pyupio/safety)
[![Bandit](docs/badges/bandit.svg)](https://github.com/PyCQA/bandit)

[![mkdocs-material](docs/badges/mkdocs-material.svg)](https://squidfunk.github.io/mkdocs-material/)
[![Celery](docs/badges/celery.svg)](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)
[![Redis Stack](docs/badges/redis.svg)](https://redis.io/docs/about/about-stack/)

See [the documentation](https://brent-stone.github.io/avengercon_2024/) for information
on using this repo. The [Avengercon VIII conference](https://avengercon.com/) 
homepage has details about the event.

---
This is a hands-on Python programming workshop. At least one year of recent Python 
experience, some experience with Docker, and a computer you administer is strongly 
recommended.

Python can be challenging to use in production when "real-world" workloads involving 
megabits per second (Mbps) of streaming data or terabytes of stored data are involved. 
The Global Interpreter Lock (GIL) means that a Python interpreter is effectively 
single-threaded and can't take advantage of modern processors' capacity for parallel 
computation. Laterally scaling workloads across many Python interpreters is one of the 
most viable workarounds to the shortcomings of the GIL. This workshop will introduce you
to two leading frameworks for doing this: Celery, Dask, and Apache Beam. 
This workshop will walk through establishing an Extract, Transform, Load (ETL) pipeline 
in each framework which reads and writes from Redis and a MinIO locally hosted S3 
bucket.