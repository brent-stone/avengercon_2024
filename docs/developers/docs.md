## mkdocs-material

This project uses [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) to
manage and dynamically generate documentation as a set of static websites.

To generate and view the compiled documentation locally, run the following
within the activated poetry virtual environment:

```bash
mkdocs build
```
```bash
mkdocs serve
```

### Admonitions
The [admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions)
extension is used to provide callouts. The
[list of available admonitions](https://docutils.sourceforge.io/docs/ref/rst/directives.html#specific-admonitions)
is available to customize callouts.

Examples:

!!! note
    This is a note.

!!! warning
    This is a warning.

### Example Sites Using Mkdocs-Material

* [up42](https://github.com/up42/up42-py/tree/master) is a nice example of customizing
mkdocs-material defaults.