## Alembic Database Migration tips
- Auto-generate a database revision
  - `alembic revision --autogenerate -m "Added table XYZ"`
  - Look in alembic > versions for the revision and validate/update as needed.
  - Implement the revision with `alembic upgrade head`

## [SQLAlchemy Mapped Class](https://docs.sqlalchemy.org/en/latest/orm/mapper_config.html)
The [walkthrough of SQLAlchemy 2.0 Declarative Mapping](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#declarative-mapping) helps quickstart correct design pattern understanding.

1. [Declaring a One-to-Many Relationship](https://docs.sqlalchemy.org/en/20/orm/cascades.html#using-foreign-key-on-delete-cascade-with-orm-relationships) with cascading deletion.
2. [Declaring a Many-to-Many relationship](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#setting-bi-directional-many-to-many) with unique constraints.
3. [Use mixins](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#mixing-in-columns) for recurring column name/types like `updated_on` datetimes.
!!! note
    The mixin example references `func.now()` which isn't pseudocode. Use `from sqlalchemy import func`.
4. [Combining dataclass & mixins](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#using-mixins-and-abstract-superclasses) features

## SQLAlchemy Types
The [SQLAlchemy Type](https://docs.sqlalchemy.org/en/20/core/types.html) system supports
both generic and backend specific types.

`mapped_column()` [has implied associations](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#using-annotated-declarative-table-type-annotated-forms-for-mapped-column)
between SQLAlchemy types and basic Python types which can be customized.