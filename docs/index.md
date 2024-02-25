# Avengercon VIII Workshop <br> Horizontally Scaling Python for Production

Repo Status </br>
![Tests](badges/tests.svg)
![Coverage](badges/coverage.svg)
![Interrogate](badges/interrogate_badge.svg)
<!---
Update the CI status to your repo's project name!
https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge
https://docs.gitlab.com/ee/user/project/badges.html#view-the-url-of-pipeline-badges
-->
<!---
Helpful sites for repo badges
https://shields.io/
https://simpleicons.org
https://github.com/NWylynko/react-simple-badges/blob/main/badges.md
-->

Tooling </br>
![Python](badges/python311.svg)
[![Poetry](badges/poetry.svg)](https://python-poetry.org/)
[![Tox](badges/tox.svg)](https://tox.wiki/)
[![Black](badges/black.svg)](https://black.readthedocs.io/en/stable/)
[![Safety](badges/safety.svg)](https://github.com/pyupio/safety)
[![Bandit](badges/bandit.svg)](https://github.com/PyCQA/bandit)

[![Celery](badges/celery.svg)](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)
[![Dask](badges/dask.svg)](https://www.dask.org/)
[![Apache Beam](badges/beam.svg)](https://beam.apache.org/#)
[![Redis Stack](badges/redis.svg)](https://redis.io/docs/about/about-stack/)
[![MinIO](badges/minio.svg)](https://min.io/)
[![mkdocs-material](badges/mkdocs-material.svg)](https://squidfunk.github.io/mkdocs-material/)

**Workshop Date**: 28 February 2024

The [Avenercon VIII conference](https://avengercon.com/)
homepage has details about the event where this workshop was held.

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