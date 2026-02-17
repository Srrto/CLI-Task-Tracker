import os
from datetime import date
from datetime import datetime
import json
os.system("cls")

#Constants
FILE_NAME = "tasks.json"
FORMAT_DATE = datetime.now().strftime('Dia: %d, Mes: %m, Año: %Y, A las %H:%M')
status_list = ["To do", "In-Progress", "Completed"]

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
    existing_ids = sorted(task["id"] for task in tasks)
    new_id = 1
    for task_id in existing_ids:
        if task_id == new_id:
            new_id += 1
        else:
            break
        
    return new_id
            
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
    
#print tasks
def print_tasks():
    tasks = load_tasks()
    for t in tasks:
        print(f"{t}\n")

#update tasks
def update_task():
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
def change_progress():
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
        save_tasks(tasks)
        print("Progress updated sucessfully")
    else:
        print("Progress value not valid. Changes no made")
            
      
#Command executions

change_progress()