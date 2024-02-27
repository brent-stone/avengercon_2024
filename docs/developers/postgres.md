## PostgreSQL Container Management

### Troubleshooting Postgres container authentication
- It's necessary to prune both containers and volumes related to postgres to easily
reset the initial settings.
- You'll know you adequately reset the postgres container build to grab new settings
if you see `CREATE DATABASE` and extraordinarily long output generated when starting the
container.
- To see the values of a custom enumerated type in Adminer or postgres command line, run
the following sql query: `SELECT enum_range(NULL::<custom_type_name>)`
