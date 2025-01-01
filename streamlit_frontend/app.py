import streamlit as st
import requests

# Base URL
API_BASE_URL = "http://127.0.0.1:8000/api/"
REGISTER_API = f"{API_BASE_URL}register/"
LOGIN_API = f"{API_BASE_URL}login/"

def get_events():
    response = requests.get(f"{API_BASE_URL}events/")
    if response.status_code == 200:
        return response.json()
    st.error("Failed to fetch events.")
    return []

def get_tasks():
    response = requests.get(f"{API_BASE_URL}tasks/")
    if response.status_code == 200:
        return response.json()
    st.error("Failed to fetch tasks.")
    return []

def get_attendees():
    response = requests.get(f"{API_BASE_URL}attendees/")
    if response.status_code == 200:
        return response.json()
    st.error("Failed to fetch attendees.")
    return []

def create_event(event_data):
    response = requests.post(f"{API_BASE_URL}events/", json=event_data)
    if response.status_code == 201:
        st.success("Event created successfully!")
        return response.json()
    st.error("Failed to create event.")
    return None

def create_task(task_data):
    response = requests.post(f"{API_BASE_URL}tasks/", json=task_data)
    if response.status_code == 201:
        st.success("Task created successfully!")
        return response.json()
    st.error(f"Failed to create task.Server responded with: {response.status_code} - {response.text}")
    return None

def create_attendee(attendee_data):
    response = requests.post(f"{API_BASE_URL}attendees/", json=attendee_data)
    if response.status_code == 201:
        st.success("Attendee created successfully!")
        return response.json()
    st.error("Failed to create attendee.")
    return None

def delete_event(event_id):
    response = requests.delete(f"{API_BASE_URL}events/{event_id}/")
    if response.status_code == 204:
        st.success("Event deleted successfully!")
    else:
        st.error("Failed to delete event.")

def delete_task(task_id):
    response = requests.delete(f"{API_BASE_URL}tasks/{task_id}/")
    if response.status_code == 204:
        st.success("Task deleted successfully!")
    else:
        st.error("Failed to delete task.")

def delete_attendee(attendee_id):
    response = requests.delete(f"{API_BASE_URL}attendees/{attendee_id}/")
    if response.status_code == 204:
        st.success("Attendee deleted successfully!")
    else:
        st.error("Failed to delete attendee.")

def create_assignment(assignment_data):
    response = requests.post(f"{API_BASE_URL}assignments/", json=assignment_data)
    if response.status_code == 201:
        st.success("Attendee assigned successfully!")
        return response.json()
    else:
        st.error(f"Failed to assign attendee. Error: {response.text}")
    return None
  
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = requests.post(LOGIN_API, json={"username": username, "password": password})
        if response.status_code == 200 and response.json().get("status") == "success":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.is_admin = response.json().get("is_admin", False)
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error(response.json().get("message", "Failed to log in"))

def register():
    st.title("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        try:
            response = requests.post(REGISTER_API, json={"username": username, "password": password})
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get("status") == "success":
                        st.success("Registration successful! Please log in.")
                        st.rerun()
                    else:
                        st.error(data.get("message", "Failed to register"))
                except ValueError:
                    st.error("Failed to decode response, expected JSON but got something else.")
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
            
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    
if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.success("You have been logged out!")
    st.rerun()

if not st.session_state["logged_in"]:
    auth_page = st.sidebar.radio("Authentication", ["Login", "Register"])
    if auth_page == "Login":
        login()
    elif auth_page == "Register":
        register()
else:
# Streamlit App Layout
    st.title("Event Management Dashboard")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Event Management", "Task Management", "Attendee Management"])

    # Event Management Page
    if page == "Event Management":
        st.header("Event Management")
        
        # Display Event List
        st.subheader("Event List")
        events = get_events()
        for event in events:
            st.write(f"**{event['name']}**")
            st.write(f"Description: {event['description']}")
            st.write(f"Location: {event['location']}")
            st.write(f"Date: {event['date']}")
            if st.button(f"Delete {event['name']}", key=f"delete_event_{event['id']}"):
                delete_event(event['id'])
        
        # Add New Event
        st.subheader("Add New Event")
        with st.form(key="add_event_form"):
            name = st.text_input("Name")
            description = st.text_area("Description")
            location = st.text_input("Location")
            date = st.date_input("Date")
            submit_event = st.form_submit_button(label="Add Event")
        
        if submit_event:
            if not name or not description or not location or not date:
                st.error("All fields are required!")
            else:
                event_data = {
                    "name": name,
                    "description": description,
                    "location": location,
                    "date": str(date),
                }
                create_event(event_data)

    # Task Management Page
    elif page == "Task Management":
        st.header("Task Management")
        st.subheader("Task List")
        tasks = get_tasks()
        event_choices = {event['name']: event['id'] for event in get_events()}
        selected_event = st.selectbox("Select Event", options=list(event_choices.keys()))

        filtered_tasks = [task for task in tasks if task['event'] == event_choices[selected_event]]
        completed_tasks = 0

        for task in tasks:
            st.write(f"**{task['title']}**")
            st.write(f"Description: {task['description']}")
            st.write(f"Status: {task['status']}")
            status_update = st.selectbox(f"Update Status for {task['title']}", options=["Pending", "Completed"], index=0 if task['status'] == "Pending" else 1, key=f"status_{task['id']}")
            
            if st.button(f"Update Status for {task['title']}", key=f"update_status_{task['id']}"):
                task_data = requests.get(f"{API_BASE_URL}tasks/{task['id']}/").json()
                #log
                print(f"Task data response: {task_data}")
                updated_task_data = {
                    "title": task_data["title"],
                    "description": task_data["description"],
                    "status": status_update,
                    "event": task_data["event"],  
                    "assignments": task_data["assignments"]  
                }
                print(f"{updated_task_data}")
                response = requests.patch(f"{API_BASE_URL}tasks/{task['id']}/", json=updated_task_data)
                if response.status_code == 200:
                    st.success(f"Status of task '{task['title']}' updated to {status_update}.")
                    st.rerun()
                else:
                    st.error(f"Failed to update task status: {response.status_code} - {response.text}")
            assignments = task.get("assignemnts",[]) # Make sure `assignments` is properly queried
            for assignment in assignments:
              st.write(f"Assigned to: {assignment['attendee']['name']}")            
            if st.button(f"Delete {task['title']}", key=f"delete_task_{task['id']}"):
                delete_task(task['id'])
            if task["status"].lower() == "completed":
              completed_tasks += 1
        total_tasks = len(filtered_tasks)
        if total_tasks > 0:
            progress_percentage = (completed_tasks / total_tasks) * 100
            st.subheader("Task Progress")
            st.progress(progress_percentage / 100)
            st.write(f"Progress: {completed_tasks}/{total_tasks} tasks completed.")
        else:
            st.write("No tasks available for the selected event.")
            
        st.subheader("Add New Task")
        with st.form(key="add_task_form"):
            title = st.text_input("Title")
            description = st.text_area("Description")
            status = st.selectbox("Status", ["Pending", "Completed"])
            
            events = get_events()
            event_choices = {event['name']: event['id'] for event in events}
            selected_event = st.selectbox("Select Event", options=list(event_choices.keys()))
            
            attendees = get_attendees()
            attendee_choices = {attendee['name']: attendee['id'] for attendee in attendees}
            selected_attendee = st.selectbox("Assign Attendee", options=list(attendee_choices.keys()))
            
            submit_task = st.form_submit_button(label="Add Task")
        
        if submit_task:
            if not title or not description or not selected_event or not selected_attendee:
                st.error("All fields are required!")
            else:
                task_data = {
                    "title": title,
                    "description": description,
                    "status": status,
                    "event": event_choices[selected_event],
                    "assignments":[]
                    # "attendee": attendee_choices[selected_attendee],
                    # "assignments": [
                    #       {
                    #           "event": event_choices[selected_event],
                    #           "task": None,  
                    #           "attendee": attendee_choices[selected_attendee],
                    #       }
                    # ]git
                }
                new_task = create_task(task_data)
                if new_task:  
                  assignment_data = {
                      "event": event_choices[selected_event],
                      "task": new_task['id'], 
                      "attendee": attendee_choices[selected_attendee],
                  }
                  create_assignment(assignment_data) 

    # Attendee Management Page
    elif page == "Attendee Management":
        st.header("Attendee Management")
        
        st.subheader("Attendee List")
        attendees = get_attendees()
        for attendee in attendees:
            st.write(f"**{attendee['name']}**")
            st.write(f"Email: {attendee['email']}")
            st.write(f"Phone: {attendee['phone_number']}")
            if st.button(f"Delete {attendee['name']}", key=f"delete_attendee_{attendee['id']}"):
                delete_attendee(attendee['id'])
        
        st.subheader("Add New Attendee")
        with st.form(key="add_attendee_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone_number = st.text_input("Phone Number")
            submit_attendee = st.form_submit_button(label="Add Attendee")
        
        if submit_attendee:
            if not name or not email or not phone_number:
                st.error("All fields are required!")
            elif not email.count("@") or not email.count("."):
                st.error("Invalid email format!")
            elif not phone_number.isdigit():
                st.error("Phone number must be numeric!")
            else:
                attendee_data = {
                    "name": name,
                    "email": email,
                    "phone_number": phone_number,
                }
                create_attendee(attendee_data)
        
        st.subheader("Assign Attendee to Event/Task")
        with st.form(key="assign_attendee_form"):
          event_choices = {event['name']: event['id'] for event in get_events()}
          selected_event = st.selectbox("Select Event", options=list(event_choices.keys()))
          
          task_choices = {task['title']: task['id'] for task in get_tasks()}
          selected_task = st.selectbox("Select Task", options=list(task_choices.keys()))
          
          attendee_choices = {attendee['name']: attendee['id'] for attendee in get_attendees()}
          selected_attendee = st.selectbox("Select Attendee", options=list(attendee_choices.keys()))
          
          submit_assignment = st.form_submit_button(label="Assign Attendee")

        if submit_assignment:
          assignment_data = {
              "event": event_choices[selected_event],
              "task": task_choices[selected_task],
              "attendee": attendee_choices[selected_attendee],
          }
          create_assignment(assignment_data)

        