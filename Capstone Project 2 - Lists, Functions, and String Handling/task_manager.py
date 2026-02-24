# Note use the following username and password to access the admin rights 
# username: admin
# password: password
#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''Here you will write code that will allow a user to login.
    - Your code must read usernames and password from the user.txt file
    - You can use a list or dictionary to store a list of usernames and passwords from the file.
    - Use a while loop to validate your user name and password.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


# Defining the functions to be used in the following options.

# Register a new user.
def reg_user():
    # - Request input of a new username
    new_username = input("New Username: ")

    # Check that this username doesn't exist already.
    while new_username in username_password.keys():
        print("That username already exists. Please choose another.")
        new_username = input("New Username: ")

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password
            
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")


# The following code, for updating tasks.txt, get re-used a few times, so
# I've decided to abstract it.
def update_tasks():
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))


# Add a task.
def add_task():
    # - Prompt a user for the following: 
    #     - A username of the person whom the task is assigned to,
    #     - A title of a task,
    #     - A description of the task and 
    #     - the due date of the task.
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        add_task() # Instead of continue, which won't work after refactoring.
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")


    # - Then get the current date.
    curr_date = date.today()
    # - Add the data to the file task.txt and
    # - You must remember to include the 'No' to indicate if the task is complete.
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)

    update_tasks()

    print("Task successfully added.")


# View all tasks.
def view_all():
    '''In this block you will put code so that the program will read the task from task.txt file and
    print to the console in the format of Output 2 presented in the task pdf (i.e. include spacing and labelling) 
    You can do it in this way:
    - Read a line from the file.
    - Split that line where there is comma and space.
    - Then print the results in the format shown in the Output 2 
    - It is much easier to read a file using a for loop.'''
    print("-----------------------------------")
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)
        print("-----------------------------------")


# Mark a task as completed.
def mark_complete(task):
    task['completed'] = True
    update_tasks()
    print("Task marked as complete.")


# Reassign a task
def reassign(task, user):
    task['username'] = user
    update_tasks()
    print(f"The task has been reassigned to {user}.")



# Change the due date of a task.
def change_date(task, date):
    task['due_date'] = datetime.strptime(date, DATETIME_STRING_FORMAT)
    update_tasks()
    print(f"The task is now due on {date}.")


# View your own tasks.
# Makes use of mark_complete/1, reassign/2 and change_date/2
def view_mine():
    '''In this block you will put code so that the program will read the task from task.txt file and
    print to the console in the format of Output 2 presented in the task pdf (i.e. include spacing and labelling) 
    You can do it in this way:
    - Read a line from the file.
    - Split that line where there is comma and space.
    - Then print the results in the format shown in the Output 2 
    - It is much easier to read a file using a for loop.'''
    print("-----------------------------------")
    accessible_refs = [-1] # for returning to the main menu later
    for count, task in enumerate(task_list):
        if task['username'] == curr_user:
            accessible_refs.append(count) # for use as a reference number
            disp_str = f"Task ref.: \t {count}\n"
            disp_str += f"Task: \t\t {task['title']}\n"
            disp_str += f"Assigned to: \t {task['username']}\n"
            disp_str += f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {task['description']}\n"
            disp_str += f"Completed? \t "
            disp_str += "Yes\n" if task['completed'] else "No\n"
            print(disp_str)
            print("-----------------------------------")

    task_selection = int(input(
'''Select a task reference number to edit, or -1 to return to the main menu.
'''))

    # Check the user has made a valid selection.
    while task_selection not in accessible_refs:
        print("Selection not recognized.")
        task_selection = int(input(
'''Select a task reference number to edit, or -1 to return to the main menu.
'''))

    while task_selection != -1:
        edit_options = input(
'''Choose from the following options.
c - mark the task as complete
e - edit the task
x - exit this menu
''')
        # Mark the task complete
        if edit_options == "c":
            mark_complete(task_list[task_selection])
            break
        
        # Edit the task
        elif edit_options == "e":
            if task_list[task_selection]['completed']:
                print(
'''This task cannot be edited, as it has already been completed.''')
            
            else:
                # Options for editing the task
                how_edit = input('''
Choose from the following options.
u - change the username of the person assigned to the task
d - change the due date of the task
x - exit this menu
''')
                # Reassign the task
                if how_edit == "u":
                    user_now = input(
            '''Enter the username of the person assigned to the task.\n''')
                    
                    # Check that the username exists.
                    while user_now not in username_password.keys():
                        print("That username is not recognized.")
                        user_now = input(
            '''Enter the username of the person assigned to the task.\n''')
                    
                    reassign(task_list[task_selection], user_now)

                #  Change the due date
                elif how_edit == "d":
                    date_now = input(
                    '''What is the due date for the task (YYYY-MM-DD)?\n''')

                    # Check for appropriate date format.
                    while not(date_now[:4].isdigit() 
                    and date_now[5:7].isdigit() and date_now[8:].isdigit() 
                    and date_now[4] == "-" and date_now[7] == "-"):
                        print("Invalid date format.")
                        date_now = input(
                    '''What is the due date for the task (YYYY-MM-DD)?\n''')

                    change_date(task_list[task_selection], date_now)
                
                elif how_edit == "x":
                    break
                
                else:
                    print("Selection not recognized.")
        
        elif edit_options == "x":
            break
        
        else:
            print("Selection not recognized.")
        

# Here are the functions for generating reports.

# The function for generating task_overview.txt.
def generate_task_overview():

    # We get the necessary figures.
    tasks_generated = len(task_list)
    tasks_completed = len(list(filter(lambda x: x['completed'], task_list)))
    tasks_incomplete = tasks_generated - tasks_completed
    tasks_overdue = len(list(filter(lambda x: (not x['completed'])
     and x['due_date'].date() < date.today(), task_list)))
    percentage_incomplete = round((float(tasks_incomplete) / tasks_generated)
     * 100, 2)
    percentage_overdue = round((float(tasks_overdue) / tasks_generated) * 100,
     2)

    # We write the figures to an output file.
    overview_str = "Task Overview\n--------------------------------------\n"
    overview_str += f"Tasks generated: \t {tasks_generated}\n"
    overview_str += f"Completed tasks: \t {tasks_completed}\n"
    overview_str += f"Uncompleted tasks: \t {tasks_incomplete}\n"
    overview_str += f"{percentage_incomplete}% of all tasks are uncompleted\n"
    overview_str += f"Overdue tasks: \t\t {tasks_overdue}\n"
    overview_str += f"{percentage_overdue}% of all tasks are overdue"

    with open("task_overview.txt", "w") as task_overview:
        task_overview.write(overview_str)
    
    # Reassurance
    print("The task overview has been generated.")


# The function for generating user_overview.txt.
def generate_user_overview():

    # Get the figures
    users = len(user_data)
    tasks = len(task_list)

    # Create a dictionary to record how many tasks have been assigned to each user.
    user_tasks = {}
    for user in username_password.keys():
        '''counter = 0
        for task in task_list:
            if task['username'] == user:
                counter += 1'''
        user_tasks[user] = len(list(filter(lambda x: x['username'] == user,
         task_list)))
    
    overview_str = "User overview\n--------------------------------------\n"
    overview_str += f"Users registered: \t {users}\n"
    overview_str += f"Tasks generated: \t {tasks}\n"
    
    for user in user_tasks:

        # Individual statistics
        their_tasks = user_tasks[user]
        their_completed = len(list(filter(lambda x: x['username'] == user
         and x['completed'], task_list)))
        their_overdue = len(list(filter(lambda x: x['username'] == user
         and (not x['completed']) and x['due_date'].date() < date.today(),
          task_list)))
        pct_of_total = round((float(their_tasks) / tasks) * 100, 2)
        pct_complete = round((float(their_completed) / their_tasks) * 100, 2)
        pct_uncomplete = 100 - pct_complete
        pct_overdue = round((float(their_overdue) / their_tasks) * 100, 2)
        
        # Output string
        overview_str += f"\n{user}\n"
        overview_str += f"Tasks assigned: \t {their_tasks}\n"
        overview_str += f"...{pct_of_total}% of all tasks assigned\n"
        overview_str += f"{pct_complete}% of this user's tasks "
        overview_str += "have been completed.\n"
        overview_str += f"{pct_uncomplete}% of this user's tasks "
        overview_str += "have not been completed.\n"
        overview_str += f"{pct_overdue}% of this user's tasks "
        overview_str += "are currently overdue.\n"
        
    # Generate the output
    with open("user_overview.txt", "w") as user_overview:
        user_overview.write(overview_str)
    
    # Reassurance
    print("The user overview has been generated.")


# Display statistics
def display_stats():
    
    # Generate any overview files that don't exist yet.
    if not os.path.exists("task_overview.txt"):
        generate_task_overview()
    
    if not os.path.exists("user_overview.txt"):
        generate_user_overview()

    # Read the two files.
    print("\n")

    with open("task_overview.txt", "r") as task_overview:
        for line in task_overview.readlines():
            print(line.strip("\n"))

    print("--------------------------------------\n\n")
    
    with open("user_overview.txt", "r") as user_overview:
        for line in user_overview.readlines():
            print(line.strip("\n"))



while True:
    #presenting the menu to the user and 
    # making sure that the user input is coneverted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my tasks
gr - generate reports
ds - display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'gr':
        generate_task_overview()
        generate_user_overview()
    
    elif menu == 'ds':
        display_stats()
    
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")