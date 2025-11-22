# ENSAI BDE – CLI Application for Managing Events

This project implements a command-line application used to manage events organized by the ENSAI Student Union (BDE).  
It is built using an object-oriented layered architecture, a PostgreSQL database, and is fully tested with pytest.

🎯 **Project Objective**

The application allows ENSAI students to browse and register for events organized by the BDE.  
Administrators can create events as well as buses associated with these events.


## :arrow_forward: Software and tools

- Visual Studio Code  
- Python 3.x  
- PostgreSQL  
- Git  


## :arrow_forward: Clone the repository

- [ ] Open VSCode  
- [ ] Open **Git Bash**  
- [ ] Clone the repo  
  - `git clone https_link_to_repo` *(to be adapted)*


### Open Folder

- [ ] Open **Visual Studio Code**  
- [ ] File > Open Folder  
- [ ] Select the cloned project folder  
  - The folder you select should be the root of your Explorer  
  - :warning: If not, the application may not launch properly  


## Repository Files Overview

| Item                    | Description                                                                  |
| ----------------------- | ---------------------------------------------------------------------------- |
| `README.md`             | Provides useful information to present, install, and use the application    |
| `requirements.txt`      | Lists the required Python packages                                           |
| `.vscode/settings.json` | Configured to run the code from the `src` directory                          |
| `.env`                  | Must be created to configure PostgreSQL connection variables                 |


### Folders

| Folder   | Description                                                        |
| -------- | ------------------------------------------------------------------ |
| `data`   | Contains SQL scripts (`init_db.sql`, `pop_db.sql`)                 |
| `doc`    | UML diagrams and weekly reports                                    |
| `src`    | Python files using a layered architecture + all tests              |


## :arrow_forward: Install required packages

- [ ] In Git Bash, run:

```bash
pip install -r requirements.txt
:arrow_forward: Environment variables
```

At the root of the project:

- Create a .env file

 Paste in and complete the elements below:
```
POSTGRES_HOST=your_host
POSTGRES_PORT=5432
POSTGRES_DATABASE=your_database
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_SCHEMA=your_schema
```

## :arrow_forward: Database Initialization

To initialize the database:

Create the database schema:

```
psql -h <HOST> -p <PORT> -U <USER> -d <DATABASE> -f data/init_db.sql
```

Insert initial data:
```
psql -h <HOST> -p <PORT> -U <USER> -d <DATABASE> -f data/pop_db.sql
```
## :arrow_forward: Launch the CLI application

To start the application:

python src/main.py

## :arrow_forward: Main Features
👤 User (ENSAI Student)

Create an account or log in

Browse available events

Register for an event using its ID

🛠️ Administrator (BDE Member)

Create events

Create buses

View the full list of events
View the full list of customers
Delete an event

## :arrow_forward: Project Architecture

The application follows a three-layer architecture for modularity and clarity.

1. Business Objects (Models)
### File	Description
bus.py	Represents a bus (linked event, description…)
evenement.py	Represents an event (date, time, description…)
inscription.py	Represents a registration
utilisateur.py	Represents a user
2. DAO (Data Access Objects)
### File	Purpose
utilisateur_dao.py	User creation, insertion, verification
evenement_dao.py	Event management (create, list, delete…)
inscription_dao.py	Registration management
bus_dao.py	Bus management
3. Services

Contains business logic and coordinates DAO calls to perform actions.

4. View (Command-Line Interface)

CLI modules interacting with the user:

creer_compte_vue.py

page_utilisateur_vue.py

page_admin_vue.py

menu_vue.py

## :arrow_forward: Unit tests

Tests are organized in the following folders:
```
src/tests/tests_business/

src/tests/tests_dao/

src/tests/tests_service/
```

Run all tests
```
pytest -v --color=yes
```

Run a specific test

Example:
```
pytest src/tests/test_service/test_utilisateur_service.py
```
## :arrow_forward: Database
File	Description
init_db.sql	Initializes the PostgreSQL schema and tables
pop_db.sql	Inserts initial data (e.g., a first user)

Main tables: users, buses, events, registrations.

## :arrow_forward: Technologies Used

Python 3.x

PostgreSQL

Environment Management with .env

Pytest

Command-Line Interface (CLI)