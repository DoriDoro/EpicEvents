# Epic Events

## Description:
Project 12 OpenClassrooms Path - Epic Events -- develop a secure back-end architecture with Python and SQL

Work in progress ...

using SQLite for the evaluation and
one other branch project with PostgreSQL


## Installation:
open terminal
1. `git clone https://github.com/DoriDoro/EpicEvents.git`
2. `cd EpicEvents`
3. `python3 -m venv venv`
4. `. venv/bin/activate` on MacOS and Linux `venv\Scripts\activate` on Windows
5. `pip install -r requirements.txt`

Option 1: <br>
start the program with command: `python manage.py start` and login with one of these emails:

  |    **Employee email**     |    Password     |  Role  |
  |:-------------------------:|:---------------:|:------:|
  |   john.turner@mail.com    |  TestPassw0rd!  |   SA   |
  |   john.jacobs@mail.com    |  TestPassw0rd!  |   SU   |
  |  joseph.osborne@mail.com  |  TestPassw0rd!  |   MA   |


Option 2: <br>
create additional fake data by yourself, by running these commands:
1. `python manage.py data_create_employee` (prints one employee/user email on console to login)
2. `python manage.py data_create_client`
3. `python manage.py data_create_contract`
4. `python manage.py data_create_event`

the commands to create all these data is located in `data/management/commands/`


## Skill:
- Implementing a secure database with Python and SQL


## Visualisation:
