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

**Option 1:** <br>
start the program with command: `python manage.py start` and login with one of these emails:

  |    **Employee email**     |    Password     |  Role  |
  |:-------------------------:|:---------------:|:------:|
  |   john.turner@mail.com    |  TestPassw0rd!  |   SA   |
  |   john.jacobs@mail.com    |  TestPassw0rd!  |   SU   |
  |  joseph.osborne@mail.com  |  TestPassw0rd!  |   MA   |


**Option 2:** <br>
create fake data by yourself, by running these commands:
1. `python manage.py data_create_employee` (prints one employee/user email, with Role: SA, on console to log in)
2. `python manage.py data_create_client`
3. `python manage.py data_create_contract`
4. `python manage.py data_create_event`

the commands to create all these data is located in `data/management/commands/`.


## Skill:
- Implementing a secure database with Python and SQL


## Visualisation:
After loging in with email and password, you will be redirected to the command: `python manage.py start` and you choose from a menu what you want to do: <br>
![start](/README_images/EpicEvents_start.png)

Every employee, regardless of their role, can list all employees, all clients, all contracts and all events. This list appears as ready only. <br>
![list](/README_images/EpicEvents_listEmployees.png)

As described every employee can list all, but certain can filter further. After the listing of the model, an input appears to ask if this employee wants to filter.
If the employee chooses 'yes' and have the permission to filter, the employee can filter the model. <br>
![list_filter](/README_images/EpicEvents_listContracts.png)

After choosing to filter and permission granted, the employee can choose one to several model attributes to filter the events. <br>
![filter](/README_images/EpicEvents_filterEvents.png)

This picture demonstrate the creation of a client. <br>
![create](/README_images/EpicEvents_createClient.png)

To update a model instance, a little table displays all details of the model instance. The employee can choose, from one to multiple, which field the employee wants to update. 
The updated data will be displayed right after the update of the model instance. <br> 
![update](/README_images/EpicEvents_updateContract.png)


To demonstrate the data creation: 
![data](/README_images/EpicEvents_data_creation.png)
