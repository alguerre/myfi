## Tasks
### Data
- [ ] ~~Pick all categories from 2019~~
- [ ] Generate a dummy data/source_*.xls file
- [ ] Manual categorization of bizum and transfers
### Database
- [x] Use foreign key for categories
- [x] Create tables from SQLAlchemy models
- [x] Modify raw queries for ORM
- [ ] Migrations to avoid table regeneration -> alembic
### Domain logic
- [x] Bug in number of insertions
- [x] Identify savings better
  - [x] foreign key to finance in savings table
- [ ] Include other banks 
  - Create repositories
- [ ] ~~Avoid updating twice the savings table~~ savings table is removed
### GUI
- [x] Create GUI with streamlit
  - [x] Create containers
  - [x] Fix text issues in plots
- [x] Launch gui from cli
- [x] Include filters in dataframe
### Structure
- [x] Repository with queries
- [x] Decorator to manage session in cli
- [ ] Create tests
- [ ] Create a painters and repo factory
  - The proper approach would be the Unit of Work pattern
  - https://itnext.io/decoupling-python-code-implementing-the-unit-of-work-and-repository-pattern-6b3257e8b167
- [x] Add to git
- [ ] Use a set of rules for operations like
  - Exclude concepts when importing file
  - Indicate which corresponds to savings
  - This way we can create a set of user configuration files containing these rules sets and avoid hardcoding.
  - Can these rules be sent to the repository layer to do `select-where` in SQLAlchemy queries?
  - These configurations could include date and concept
  - We should have db-repositories and file-repositories
- [x] Savings table can be removed and just create new column in finances
