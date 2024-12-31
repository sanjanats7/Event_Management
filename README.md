# Event Management System

The **Event Management System** is a web application built using **Streamlit** and **Django**. It allows event organizers to create and manage events, track tasks, and assign them to participants. The system features a user-friendly interface for both event organizers and participants to manage and interact with events and tasks seamlessly.

It includes **Login/Register** and **Logout** functionality for access control.

## Key Features

- **Event Creation**: Organizers can create events by providing details like name, description, date, location, and assign tasks to participants.
- **Task Management**: Organizers can assign tasks to participants, and track their progress (pending, in progress, or completed).
- **User Authentication**: Secure login, registration, and logout options for both organizers and participants.
- **Task Filtering and Searching**: Users can filter tasks based on event or task status.

## Tech Stack

- **Streamlit**: For building the interactive web interface.
- **Django**: Backend framework for handling event and task data management.
- **SQLite/MySQL**: For database storage of event details, user data, and tasks.
- **Python**: Core programming language for the backend logic.

## Installation

### 1. Clone the repository
- git clone https://github.com/sanjanats7/Event_Management.git
- cd Event_Management
### 2. Create Virtual environment(optional)
- python3 -m venv env
- source env/bin/activate
- (On Windows, use env\Scripts\activate)
### 3. Install Dependencies
- pip install -r requirements.txt
### 4. Run database migrations
- python manage.py migrate
### 5. Create superuser(optional)
- python manage.py createsuperuser
### 6. Run frontend streamlit app
- streamlit run app.py
