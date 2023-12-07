# Event Registration
It's a project to create a web API to create and manage events using Django Rest Framework


# Operations:
- Registration
- Use django default login view
- Create a Event from admin panel
- Event Registration
    - Registered users should be able to register for an event.
    - Limit the number of available slots for each event.
    - Only authenticated users can register for events.
    - Users should only be able to unregister from events they've registered for.
- Search Functionality
    - Implement a basic search functionality that allows users to search for events based on keywords.
- Dashboard for Users
    - users can see the events they've registered for and manage their registrations.

# API Endpoints:
- List of all events
- Details of a specific event
- User registration for an event
- User's registered events


# Server run:

    - command: python manage.py runserver `127.0.0.1:8000`

## Commands

- python -m pip install -r requirements.txt
- python version: ```3.11.5```
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver
