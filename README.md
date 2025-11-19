CLI Application for Managing ENSAI BDE Events

This project implements a command-line application used to manage events organized by the ENSAI Student Union (BDE).
It is built using an object-oriented layered architecture, a PostgreSQL database, and is fully tested with pytest.

🎯 Project Objective

The application allows ENSAI students to browse and register for events organized by the BDE.
Administrators can create events as well as buses associated with these events.

▶️ Installation and Setup
📁 Folders

data — contains SQL scripts

doc — contains UML diagrams and weekly reports

src — contains Python files organized using a layered architecture. All source code and tests are located in the src/ directory.

📄 The requirements.txt file lists all required packages.
📄 The settings.json file is configured to run the code from the src directory.

1. Prerequisites

Visual Studio Code

Python 3.x

PostgreSQL

Git

2. Launch VS Code

Open VS Code.

Open Git Bash.

Clone the repository using:

git clone https_link_to_repo (to be adapted)


Open the project folder in VS Code:
File > Open Folder → select the cloned project directory
(Use this method rather than command-line navigation 🚨)

3. Install Dependencies

In Git Bash, run:

pip install -r requirements.txt

4. Environment Configuration

Create a .env file at the project root and add the PostgreSQL connection variables:

POSTGRES_HOST=your_host
POSTGRES_PORT=5432
POSTGRES_DATABASE=your_database
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_SCHEMA=your_schema

5. Database Initialization

Run data/init_db.sql to create the database schema.

Run data/pop_db.sql to insert an initial user and sample data.

▶️ Running the Application

To start the CLI application, run:

python src/main.py

🧩 Main Features
👤 User (ENSAI Student)

Create an account or log in

Browse available events

Register for an event (using its ID)

🛠️ Administrator (BDE Member)

Create events

Create buses

View the full list of events

🧱 Project Architecture

The application follows a three-layer architecture for modularity and clarity.

1. Business Objects (Models)

Contains domain classes describing the main entities:

bus.py — represents a bus (linked event, description, direction, etc.)

evenement.py — represents an event (date, time, description, etc.)

inscription.py — represents a registration (alcohol option, payment method, etc.)

utilisateur.py — represents a user (name, email, role, etc.)

2. DAO (Data Access Objects)

Handles direct interactions with the PostgreSQL database:

utilisateur_dao.py — user creation, insertion, verification

evenement_dao.py — event management (create, list, delete, etc.)

inscription_dao.py — registration management

bus_dao.py — bus management

3. Services

Contains business logic and coordinates DAO calls to execute application actions.

4. View (Command-Line Interface)

Includes the CLI interfaces interacting with the user:

creer_compte_vue.py — creates a user account

page_utilisateur_vue.py — student actions

page_admin_vue.py — admin-only actions

menu_vue.py — main entry point of the application

🧪 Unit Tests

Tests are organized into the following folders:

src/tests/tests_business/

src/tests/tests_dao/

src/tests/tests_service/

1. Run all tests
pytest -v --color=yes

2. Run a specific test

Example:

pytest src/tests/test_service/test_utilisateur_service.py


(Adapt according to the test you want to execute.)

🗄️ Database

init_db.sql — initializes the PostgreSQL schema and tables

pop_db.sql — inserts initial data (e.g., a first user)

Main tables: users, buses, events, registrations.

🧰 Technologies Used

Language: Python 3.x

Database: PostgreSQL

Environment Management: .env

Testing: Pytest

Interface: Command-Line (CLI)