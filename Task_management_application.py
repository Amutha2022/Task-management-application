# Task management application
# 11 functions [register_user(),  validate_login(),  restricted_function(),  add_task(),  view_all(),  view my tasks(),
# generate_reports(),  display_statistics(),  display_home_page(),  admin_user_pass(),   display_login()] are used,
# main- while loop

#there are two dashboards one for admin and other one for user.
#admin can login in both dashboard.
#username and password for admin ------->"admin" and "pass"(can used in both dashboard).
#only admin able to register new user.
#admin can generate reports only from admin dashboard.


from datetime import datetime,date
# dictionary to store username and password
registered_users = {}
# dictionary to store tasks
user_tasks = {}

# function to register user
def register_user():
    try:
        print("\n\t\t\t\t\t\t\tREGISTER")
        print()
        username = input("\t\t\t\t\tEnter the username: ")
        password = input("\t\t\t\t\tEnter the password: ")
        confirm_password = input("\t\t\t\t\tEnter the confirm password: ")
        try:
            with open("user.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if line != "":
                        user, pwd = line.split(";")
                        registered_users[user] = pwd
        except ValueError and FileNotFoundError:
            print("\n\t\t\t\t***File not Found***")
        if username in registered_users:
            print(f"***\n\t\t\t\t\t{username} is already registered***")
            return False
        elif password != confirm_password:
            print("\n\t\t\t\t\t***Passwords do not match***")
            return False
        else:
            registered_users[username] = password
            with open("user.txt", "a") as file:
                file.write(f"\n{username};{password}\n")
                print(f"\n\t\t\t\t\t***{username} is registered successfully***")
                return True
    except ValueError and FileNotFoundError:
        print("\n\t\t\t\t\t***Enter valid input***\n\t\t\t")
        
# function to login and validate
def validate_login(username, password):
    if username == "admin" and password == "pass":
        return True
    else:
        try:
            with open("user.txt", "r") as file:
                lines = file.readlines()
                registered_users = {line.split(";")[0]: line.split(";")[1].strip() for line in lines if line.strip() != ""}
            
            if username not in registered_users:
                print("\n\t\t\t\t\t***User does not exist***")
                return False

            elif registered_users[username] != password:
                print("\n\t\t\t\t\t***Wrong password***")
                return False

            return True

        except FileNotFoundError:
            print("\n\t\t\t\t\t***Error: user.txt file not found***")
            return False

        except ValueError:
            print("\n\t\t\t\t\t***Error: user.txt file is not formatted correctly***")
            return False
        
# function to restriction
def restricted_function(username, password):
    logged_in = validate_login(username, password)
    if logged_in or (username == "admin" and password == "pass"):
        print("\t\t\t\t\t___________Access Granted___________")
        # Your code for the restricted function goes here
    else:
        print("\n\t\t\t\t\t***Error: You must be logged in to access this feature***")
        return
    
#function to add_task    
def add_task():
    try:
        logged_in = validate_login(username, password)
        if logged_in or (username == "admin",password== "pass"):
            # Get the last task number from the user's task dictionary
            if username in user_tasks:
                task_num = len(user_tasks[username]) + 1
            # If the user does not have any tasks yet, assign task number 1
            else:
                task_num = 1

            # Get task details from user input
            task_name = input("\n\t\t\t\tEnter the task name: ")
            assign_to = input("\t\t\t\tEnter the task assign to: ")
            date_assigned = input("\t\t\t\tEnter the date assigned (dd/mm/yyyy): ")
            due_date = input("\t\t\t\tEnter the task due date (dd/mm/yyyy): ")
            task_status = input("\t\t\t\tTask is complete? Yes/No: ")
            task_description = input("\t\t\t\tEnter the task description: ")
            
            # Parse the dates using datetime.strptime
            date_assigned = datetime.strptime(date_assigned, '%d/%m/%Y').strftime('%d/%m/%Y')
            due_date = datetime.strptime(due_date, '%d/%m/%Y').strftime('%d/%m/%Y')
            
            # Add the task to the user's task dictionary
            if username not in user_tasks:
                user_tasks[username] = []
            user_tasks[username].append({
                'task_num': task_num,
                'task_name': task_name,
                'assign_to': assign_to,
                'date_assigned': date_assigned,
                'due_date': due_date,
                'task_status': task_status,
                'description': task_description
            })
            
            # Print success message
            
            print(f"\n\t\t\t\t\t**--------{task_name} successfully added--------**\n")
                    
            # Update the tasks.txt file
            with open("tasks.txt", "w") as f:
                for user, tasks in user_tasks.items():
                    f.write(f"\n{user}:\n")
                    for task in tasks:
                        f.write(f"{task['task_num']};{task['task_name']};{task['assign_to']};{task['date_assigned']};{task['due_date']};{task['task_status']};{task['description']}\n")
            
            return True
        else:
            print("\n\t\t\t\t\t***Error: You must be logged in to access this feature***")
    except ValueError:
        print("\n\t\t\t\t**Invalid date format. Please use the format dd/mm/yyyy**")
        return False
    
    except Exception as e:
        print("\n\t\t\t\t**An error occurred while adding the task:", e,"**")
        return False
    
# function to view all tasks
def view_all():
    
    try:
        logged_in = validate_login(username, password)
        if logged_in or (username == "admin",password== "pass"):
            
            with open("tasks.txt", "r") as f:
                tasks = f.readlines()
            user_tasks = []    
            for task in tasks:
                task = task.strip().split(";")
            #print(task)
                if len(task) >= 2: 
                    task_dict = {
                    "task_num": task[0],
                    "task_name": task[1],
                    "assign_to": task[2],
                    "date_assigned": task[3],
                    "due_date": task[4],
                    "task_status": task[5],
                    "description": task[6]
                }
                    user_tasks.append(task_dict)
            #print(user_tasks)

            print("\t\t\t____________________________________________________________________________________")
            print(f"\t\t\t\t\tTotal: {len(user_tasks)} tasks ")
            print("\t\t\t____________________________________________________________________________________")
            task_num = 1
            for task in user_tasks:
                print(f"\t\t\tTask Number {task_num}:\n")
                task_num += 1
                print(f"\t\t\t\t\tTask Name: {task['task_name']}")
                print(f"\t\t\t\t\tAssigned To: {task['assign_to']}")
                print(f"\t\t\t\t\tDate Assigned: {task['date_assigned']}")
                print(f"\t\t\t\t\tDue Date: {task['due_date']}")
                print(f"\t\t\t\t\tTask Status: {task['task_status']}")
                print(f"\t\t\t\t\tDescription: {task['description']}")
                print("\t\t\t____________________________________________________________________________________")
        else:
            print("Login fail")
            return False
                
    except FileNotFoundError:
        print("\n\t\t\t\t**Tasks file not found**")
    except Exception as e:
        print(f"\n\t\t\t\t**Error occurred: {e}**")
        
#function to view my tasks
def view_my_tasks():
    try:
        logged_in = validate_login(username, password)
        if logged_in or (username == "admin",password== "pass"):
            with open("tasks.txt", "r") as f:
                tasks = f.readlines()

            user_tasks = []
            task_count = 1  # initialize task counter

            for task in tasks:
                task_fields = task.strip().split(";")
                if len(task_fields) >= 7 and task_fields[2] == username:
                    task_dict = {
                        "task_num": task_count,
                        "task_name": task_fields[1],
                        "assign_to": task_fields[2],
                        "date_assigned": task_fields[3],
                        "due_date": task_fields[4],
                        "task_status": task_fields[5],
                        "description": task_fields[6]
                    }
                    user_tasks.append(task_dict)
                    task_count += 1  # increment task counter

            if not user_tasks:
                print("\n\t\t\t\t\tYou have no tasks assigned to you")
                return

            print("\t\t\t____________________________________________________________________________________")
            print(f"\t\t\t\t\tYou have {len(user_tasks)} tasks assigned to you")
            print("\t\t\t____________________________________________________________________________________")

            for task in user_tasks:
                print(f"\t\t\t\tTask Number: {task['task_num']}\n")
                print(f"\t\t\t\tTask Name: {task['task_name']}")
                print(f"\t\t\t\tAssigned To: {task['assign_to']}")
                print(f"\t\t\t\tDate Assigned: {task['date_assigned']}")
                print(f"\t\t\t\tDue Date: {task['due_date']}")
                print(f"\t\t\t\tTask Status: {task['task_status']}")
                print(f"\t\t\t\tDescription: {task['description']}")
                print("\t\t\t____________________________________________________________________________________")

            try:
                # Prompt the user to enter a task number
                selected_task_num = int(input("\t\t\t\tEnter a task number: "))

                # Validate that the selected task number is valid
                if selected_task_num < 1 or selected_task_num > len(user_tasks):
                    print("\n\t\t\t\tInvalid task number. Please enter a number between 1 and", len(user_tasks))
                    return
            except ValueError:
                print("\t\t\t\t\tPlease enter valid input")

            # Get the selected task details from the list of tasks
            selected_task = user_tasks[selected_task_num - 1]

            # Print the selected task details
            print("\n\t\t\tSelected task:")
            print(f"\t\t\t\tTask Number: {selected_task['task_num']}")
            print(f"\t\t\t\tTask Name: {selected_task['task_name']}")
            print(f"\t\t\t\tAssigned To: {selected_task['assign_to']}")
            print(f"\t\t\t\tDate Assigned: {selected_task['date_assigned']}")
            print(f"\t\t\t\tDue Date: {selected_task['due_date']}")
            print(f"\t\t\t\tTask Status: {selected_task['task_status']}")
            print(f"\t\t\t\tDescription: {selected_task['description']}")
            print("\t\t\t____________________________________________________________________________________")

            selected_task_status = selected_task['task_status']
            
            if selected_task_status == "yes":
                print("\n\t\t\t\tThis task has already been completed.")
            else:
                try:
                    action = input("\n\t\t\tChoose an action: mark as complete (type 'yes') or edit (type 'edit'): ")
                    if action == "yes":
                        selected_task['task_status'] = "yes"
                        with open("tasks.txt", "w") as f:
                            for task in user_tasks:
                                for task in user_tasks:
                                    task_str = ";".join([
                                    str( task['task_num']),
                                        task['task_name'],
                                        task['assign_to'],
                                        task['date_assigned'],
                                        task['due_date'],
                                        task['task_status'],
                                        task['description']
                                    ])
                                    f.write(task_str)
                        print("\n\t\t\t\t\t\t*****Task marked as complete*****\n")
                
                    elif action == "edit":
                        new_username = input("\n\t\t\t\tEnter the new assigned username (leave blank to keep the same): ")
                        new_due_date = input("\t\t\t\tEnter the new due date (leave blank to keep the same): ")
                        if new_username:
                            selected_task["assign_to"] = new_username
                        if new_due_date:
                            selected_task["due_date"] = new_due_date
                            
                        with open("tasks.txt", "w") as f:
                            for task in user_tasks:
                                for task in user_tasks:
                                    task_str = ";".join([
                                    str( task['task_num']),
                                        task['task_name'],
                                        task['assign_to'],
                                        task['date_assigned'],
                                        task['due_date'],
                                        task['task_status'],
                                        task['description']
                                    ])
                                    f.write(task_str)
                            print("\n\t\t\t\t\t\t*****Task edited*****\n")
                    else:
                        print("\n\t\t\t\t**Invalid action. Please try again**\n")
                except ValueError:
                    print("\n\t\t\t\t**Please enter valid input**")
        else:
            print("\n\t\t\t\t\t***Error: You must be logged in to access this feature***")
    except FileNotFoundError:
        print("\n\t\t\t\t**Tasks file not found**")
        
#function to generate reports
def generate_reports():
    try:
        logged_in = validate_login(username, password)
        if logged_in or (username == "admin",password== "pass"):
            with open("tasks.txt", "r") as f:
                tasks = f.readlines()
                total_tasks = len(tasks)
                num_completed_tasks = 0
                incomplete_count = 0
                overdue_count = 0
                today = datetime.now().strftime("%d/%m/%Y")
                for task in tasks:
                    task = task.strip().split(";")
                    if len(task) >= 2:
                        if task[5] == "yes":
                            num_completed_tasks += 1
                        if task[5] == "no":
                            incomplete_count += 1
                            due_date = datetime.strptime(task[4], "%d/%m/%Y")
                            if due_date < datetime.strptime(today, "%d/%m/%Y"):
                                overdue_count += 1
                        incomplete_percent = round((incomplete_count / total_tasks) * 100, 2)
                    overdue_percent = round((overdue_count / total_tasks) * 100, 2)
                with open("task_overview.txt", "w") as file:
                    file.write(f"\n\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    file.write(f'\t\t\t\tTask overview')
                    file.write(f"\n\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    file.write(f"Total number of tasks that have been generated and tracked by task_manager.py: {total_tasks}\n")
                    file.write(f'Total number of completed tasks: {num_completed_tasks}\n')
                    file.write(f"Total number of incomplete tasks: {incomplete_count}\n")
                    file.write(f"Percentage of tasks that are incomplete: {incomplete_percent}%\n")
                    file.write(f"Total number of tasks that are overdue: {overdue_count}\n")
                    file.write(f"Percentage of tasks that are overdue: {overdue_percent}%\n")
                
                print("\n\t\t\t\t\tTask overview file generated successfully.\n")
        
    except FileNotFoundError and UnboundLocalError:
        print("\n\t\t\t Error: tasks.txt file not found.")
        
    except ValueError:
        print("\n\t\t\t Error: tasks.txt file is not formatted correctly.")
        
#function to display statistics
def display_statistics():
    # Open user file and count total number of users
    with open("user.txt", "r") as f:
        users = f.readlines()
    
    # Open task file and count total number of tasks
    with open("tasks.txt", "r") as f:
        tasks = f.readlines()
        total_tasks = len(tasks)
        
    with open("user_overview.txt", "w") as f:
        f.write(f"\n\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        f.write(f'\t\t\t\tUser Overview')
        f.write(f"\n\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        f.write(f"\nTotal number of user registered with task_manager.py:{len(users)} \n")
        f.write(f"Total number of tasks that have been generated and tracked by task_manager.py: {total_tasks}\n\n")
        
        # Loop through each user and count their tasks
        for user in users:
            user = user.strip().split(";")
            user_tasks_list = []
            for task in tasks:
                task_data = task.strip().split(";")
                if len(task_data) > 2 and task_data[2] == user[0]:
                    user_tasks_list.append(task)
            completed_tasks = [task for task in user_tasks_list if task.strip().split(";")[5] == "yes"]
            uncompleted_tasks = [task for task in user_tasks_list if task.strip().split(";")[5] == "no"]
            overdue_tasks = [task for task in uncompleted_tasks if datetime.strptime(task.strip().split(";")[4], "%d/%m/%Y").date() < date.today()]
            
            # Calculate task statistics
            total_user_tasks = len(user_tasks_list)
            total_completed_tasks = len(completed_tasks)
            total_uncompleted_tasks = len(uncompleted_tasks)
            total_overdue_tasks = len(overdue_tasks)
            percentage_assigned = total_user_tasks / total_tasks * 100 if total_tasks > 0 else 0
            percentage_completed = total_completed_tasks / total_user_tasks * 100 if total_user_tasks > 0 else 0
            percentage_uncompleted = total_uncompleted_tasks / total_user_tasks * 100 if total_user_tasks > 0 else 0
            percentage_overdue = total_overdue_tasks / total_user_tasks * 100 if total_user_tasks > 0 else 0
    
            f.write(f"User: {user[0]}\n")
            f.write(f"Total number of tasks assigned: {total_user_tasks}\n")
            f.write(f"Percentage of tasks assigned: {percentage_assigned:.2f}%\n")
            f.write(f"Total number of tasks completed: {total_completed_tasks}\n")
            f.write(f"Percentage of tasks completed: {percentage_completed:.2f}%\n")
            f.write(f"Total number of tasks uncompleted: {total_uncompleted_tasks}\n")
            f.write(f"Percentage of tasks uncompleted: {percentage_uncompleted:.2f}%\n")
            f.write(f"Total number of tasks overdue: {total_overdue_tasks}\n")
            f.write(f"Percentage of tasks overdue: {percentage_overdue:.2f}%\n")
        print("\n\t\t\t\tUser overview and list of users with tasks have been generated.\n")    
        
# function to display homepage
def display_home_page():
    print("\n\n\t============================================================================================================")
    print("\t\t\t\t\t\tTASK MANAGEMENT APPLICATION")
    print("\t============================================================================================================")
    print("\n\t\t\t\t\tPlease select one of the following options\n")
    print("\t\t\t\t\tEnter 'u' - To Login as User")
    print("\t\t\t\t\tEnter 'a' - To Login as Admin")
    print("\t\t\t\t\tEnter 'e' - To Exit")
    
    user_input = input("\n\t\t\t\t\t\tEnter your choice: ").lower()
    print("\t\t\t____________________________________________________________________________________")
    print()
    return user_input

#function to write admin username and password in the user.txt
def admin_user_pass():
    with open("user.txt", "r") as file:
        lines = file.readlines()
        admin_exists = False
        for line in lines:
            user, password = line.strip().split(";")
            if user == "admin" and password == "pass":
                admin_exists = True
                break
        if not admin_exists:
            with open("user.txt", "a") as file:
                file.write("admin;pass\n")
        
# function to display login        
def display_login(username, password):
    if validate_login(username, password):
        print(f"\t\t\t\t\t___________Login successful___________\n")
        user_upper = username.upper()
        print("\t\t\t____________________________________________________________________________________")
        today = datetime.now().strftime("%d/%m/%Y")
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"\t\t\t{user_upper} DASHBOARD \t\t\t\t\t\t\t{today}, {current_time}")
        print("\t\t\t____________________________________________________________________________________")
        print(f"\t\t\t\t\tWELCOME TO TASK MANAGEMENT APPLICATION")
    else:
        display_home_page()
        
# main function
while True:
    try:
        user_input = display_home_page()
        admin_user_pass()

        # To exit
        if user_input == 'e':
            break

        # user login
        elif user_input == "u":
            print("\n\t\t\t\t\t\t\tLOGIN\n")
            username = input("\t\t\t\t\t\tEnter the username: ")
            password = input("\t\t\t\t\t\tEnter the password: ")
            print()

        # admin login
        elif user_input == "a":
            print("\n\t\t\t\t\t\t\tADMIN LOGIN\n")
            admin_user = input("\t\t\t\t\t\tEnter the username:")
            admin_pass = input("\t\t\t\t\t\tEnter the password:")
            print()
            try:
                if admin_user == "admin" and admin_pass == "pass":
                    today = datetime.now().strftime("%d/%m/%Y")
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print("\t\t\t___________________________________________________________________________________")
                    print(f"\t\t\tADMIN DASHBOARD \t\t\t\t\t\t{today},{current_time}")
                    print("\t\t\t___________________________________________________________________________________")
                    while True:
                        print("\t\t\t____________________________________________________________________________________")
                        print("\t\t\t\t\tPlease select one of the following options\n")
                        print("\t\t\t\t\tEnter 'a' - To Add a Task")
                        print("\t\t\t\t\tEnter 'va' - To View All Tasks")
                        print("\t\t\t\t\tEnter 'vm' - To View My Tasks")
                        print("\t\t\t\t\tEnter 'gr' - To Generate Reports")
                        print("\t\t\t\t\tEnter 'ds' - To Display Statistics")
                        print("\t\t\t\t\tEnter 'e' - To Exit")
                        print("\t\t\t____________________________________________________________________________________")
                        print("\n\t\t\t\t\tIf you want to register, enter 'r'")
                        print()
                        choice = input("\n\t\t\t\tEnter your choice: ")
                        print("\t\t\t____________________________________________________________________________________")
                        
                        if choice == "a":
                            username = "admin"
                            password= "pass"
                            add_task()

                        elif choice == "va":
                            username = "admin"
                            password= "pass"
                            view_all()

                        elif choice == "vm":
                            username = "admin"
                            password= "pass"
                            view_my_tasks()

                        elif choice == "ds":
                            username = "admin"
                            password= "pass"
                            try:
                                # Perform statistics calculation or display
                                display_statistics()
                            except FileNotFoundError:
                                try:
                                    with open("user.txt", "r") as user_file, open("tasks.txt", "r") as tasks_file:
                                        # Perform statistics calculation or display
                                        display_statistics()
                                except FileNotFoundError:
                                    # Create new user.txt and tasks.txt files
                                    with open("user.txt", "w") as user_file, open("tasks.txt", "w") as tasks_file:
                                        print("\n\t\t\t***New user.txt and tasks.txt files created***")
                                        # Perform statistics calculation or display
                                        display_statistics()

                        elif choice =="gr":
                            username = "admin"
                            password= "pass"
                            generate_reports()
                        
                        elif choice == "r":
                            register_user() 
                                
                        elif choice == "e":
                            print(f"\n\n\t\t\t\t\t\t\tGoodbye Admin!!!")
                            exit()
                        
            except (ValueError, SyntaxError, NameError):
                print("\n\t\t\t\t\t**Invalid input")
                # code to handle the exception
                print("Invalid input. Please enter a valid input.\n")
                exit()
                
        else:
            print("\n\t\t\t\t\t**Invalid input")
            exit()
        #functions  
        try:         
            while validate_login(username, password) == True:
                print("\t\t\t____________________________________________________________________________________")
                print("\t\t\t\t\tPlease select one of the following options\n")
                print("\t\t\t\t\tEnter 'a' - To Add a Task")
                print("\t\t\t\t\tEnter 'va' - To View All Tasks")
                print("\t\t\t\t\tEnter 'vm' - To View My Tasks")
                print("\t\t\t\t\tEnter 'e' - To Exit")
                user_input = input("\n\t\t\tEnter the choice: ")
                print("\t\t\t____________________________________________________________________________________")
                
                if user_input == "a":
                    add_task()

                elif user_input == "va":
                    view_all()

                elif user_input == "vm":
                    view_my_tasks()
                    
                elif user_input == "e":
                    print(f"\n\n\t\t\t\t\t\t\tGoodbye {username}!!!")
                    exit()

                else:
                    print("\t\t\t\tLogin failed. Please try again.\n")
                    exit()

        except (ValueError, SyntaxError, NameError):
            # code to handle the exception
            print("\t\t\t\tInvalid input. Please enter a valid input.")
            exit()

    except (ValueError, SyntaxError, NameError):
        # code to handle the exception
        print("\t\t\t\tInvalid input. Please enter a valid input.")
        exit()