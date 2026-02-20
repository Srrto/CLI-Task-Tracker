import os
from datetime import date
from datetime import datetime
import json
from enum import Enum
os.system("cls")

#Constants
FILE_NAME = "tasks.json"
FORMAT_DATE = datetime.now().strftime('Dia: %d, Mes: %m, Año: %Y, A las %H:%M')
status_list = ["To do", "In-Progress", "Completed"]

class state(Enum):
    ALL = 0
    TODO = 1
    IN_PROGRESS = 2
    COMPLETED = 3


#verifies the input is a valid integer
def get_int(prompt_valid):
    while True:
        try:
            return int(input(prompt_valid))
        except ValueError:
            print("Please input a valid number")

#load tasks
def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

#save the task once made the changes
def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

#create id
def _create_id():
    tasks = load_tasks()   
    return max(t["id"] for t in tasks) + 1
            
#Create new task
def create_task():
    tasks = load_tasks()
    new_task = {
                "id" : _create_id(),
                "Title": input("Input the title for the new task: \n"),
                "description" : input("Input a description for the new task:\n"),
                "status" : status_list[0],
                "created_At" : FORMAT_DATE,
                "updated_At" : FORMAT_DATE
        }
    tasks.append(new_task)
    save_tasks(tasks)
    print("Task saved")

#delete task
def delete_task():
    #we got the id to delete and we verify it is a valid int
    delete_id = get_int("type the id of the task to delete: \n")
    tasks = load_tasks()
    #we iterate tasks and compare with delete_id, if found returns True, not the value
    task = any((t for t in tasks if t["id"] == delete_id))
    
    #If the value was not found, stops the function
    if not task:
        print("No existe ninguna tarea con ese ID.\n")
        return
    
    #if the value was found, we create a new list without the task to delete
    new_tasks = [t for t in tasks if t["id"] != delete_id]
    save_tasks(new_tasks)
    
#print tasks
def print_tasks():
    tasks = load_tasks()
    for t in tasks:
        print(f"{t}\n")

#update tasks
def modify_task():
    upd_id = int(input("Ingresa el id de la tarea que quieres cambiar: \n"))
    tasks = load_tasks()
    
    for task in tasks:
        if upd_id == task["id"]:
            task["Title"] = input("Input the new title: \n")
            task["description"] = input("Input the new description: \n")
            task["updated_At"] = FORMAT_DATE
            save_tasks(tasks)
            print("Task updates succesfully!\n")
            break
    else:
        print("ID not found. Changes not made!\n")
             
#change progress of the task
def update_progress():
    tasks = load_tasks()
    #ask an int and verifies it is
    changing_id = get_int("Input the task to modify\n")
    task = next((t for t in tasks if t["id"] == changing_id), None)
    
    if not task:
        print("No task was found with the ID you entered")
        return
    
    progress_num = get_int("Ingresa un numero para cambiar el progreso de la tarea:\n To do = 0\n In-Progress = 1\n Completed = 2\n")
    
    if 0 <= progress_num <= 2:
        task["status"] = status_list[progress_num]
        task["updated_At"] = FORMAT_DATE
        save_tasks(tasks)
        print("Progress updated sucessfully")
    else:
        print("Progress value not valid. Changes no made")
     
#Filter all tasks
def filter_tasks(status_task: Enum):
    tasks = load_tasks()
    filtered_task = []
    
    if status_task == state.ALL:
        return tasks
    if status_task == state.TODO:
        filtered_task = [t for t in tasks if t["status"] == status_list[0]]
        return filtered_task
    if status_task == state.IN_PROGRESS:
        filtered_task = [t for t in tasks if t["status"] == status_list[1]]
        return filtered_task
    if status_task == state.COMPLETED:
        filtered_task = [t for t in tasks if t["status"] == status_list[2]]
        return filtered_task
    
    return filtered_task

#Show tasks
def show_tasks(state):
    filtered_tasks = filter_tasks(state)
    if not filtered_tasks:
        print("The list is empty. Nothing to show")
        return
    
    print(f"{"ID":<5} {"Title":<30} {"Status":<20}")
    print("_" * 60, "\n" )
    
    for tf in filtered_tasks:
        print(f"{tf["id"]:<5} {tf["Title"]:<30} {tf["status"]:<20} \n")
    
#middle-function to handle fuction with parameter

#dict of functions
actions_tasks = {
    "1": create_task,
    "2": delete_task,
    "3": modify_task,
    "4": update_progress,
    "5": show_tasks(0),
    "6": show_tasks(1),
    "7": show_tasks(2),
    "8": show_tasks(3),
}    
    
#Menu interactivo
def main_menu():
    while True:
        print("Welcome to my CLI Task Tracker\n")
        print("_" * 60, "\n")
        print("1. Create a new task \n")
        print("2. Delete task\n")
        print("3. Modify task\n")
        print("4. Update progress of a task\n")
        print("5. Show all tasks\n")
        print("6. Show al 'To do' tasks\n")
        print("7. Show all 'In progress' tasks\n")
        print("8. Show all 'Completed' tasks\n")
        print("9. Close\n")
        
        option = input("Type the option you want to do: ")
        if option == "9":
            print("Exiting...")
            break
        
        selected_action = actions_tasks.get(option)

        if selected_action:
            selected_action()
        else:
            "Option not valid. Try again"
        
        
        
#Command executions

