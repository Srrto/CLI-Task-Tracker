import os
from datetime import date
from datetime import datetime
import json
os.system("cls")


FILE_NAME = "tasks.json"
status_list = ["To do", "In-Progress", "Completed"]
#Initialitation
#save tasks
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
            
#load tasks
def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

#Create new task
def create_task():
    tasks = load_tasks()
    new_task = {
                "id" : _create_id(),
                "Title": input("Ingresa el titulo de tu tarea: \n"),
                "description" : input("Ingresa una descripcion para tu nueva tarea:\n"),
                "status" : status_list[0],
                "created_At" : datetime.now().strftime('Dia: %d, Mes: %m, Año: %Y, A las %H:%M'),
                "updated_At" : datetime.now().strftime('Dia: %d, Mes: %m, Año: %Y, A las %H:%M')
        }
    tasks.append(new_task)
    save_tasks(tasks)
    print("Task saved")
    
#print tasks
def print_tasks():
    tasks = load_tasks()
    for t in tasks:
        print(f"{t}\n")

def update_task():
    upd_id = int(input("Ingresa el id de la tarea que quieres cambiar: \n"))
    tasks = load_tasks()
    
    for task in tasks:
        if upd_id == task["id"]:
            task["Title"] = input("Ingresa tu nuevo titulo: \n")
            task["description"] = input("Ingresa tu nueva descripcion: \n")
            task["updated_At"] = datetime.now().strftime('Dia: %d, Mes: %m, Año: %Y, A las %H:%M')
            save_tasks(tasks)
            print("Tarea actualizada correctamente!\n")
            break
    else:
        print("No se encontro el id ingresado. Sin cambios!\n")
                
def change_progress():
    tasks = load_tasks()
    while True:
        try:
            changing_id = int(input("Ingresa el id de la tarea a cambiar: \n"))
            progress_num = int(input("ingresa un valor para el cambio de progreso: \n To do = 0 \n In-progress = 1 \n Completed = 2 \n"))
            break
        except ValueError:
            print("Ingresa un valor correcto para el id")
            
    for t in tasks:
        if changing_id == t["id"]:
            if progress_num >= 0 and progress_num <= 2:
                t["status"] = status_list[progress_num]
                break
            else:
                print("No existe un valor ese progreso. Sin cambios hechos")
                break
    else:
        print("No existe es id. Sin cambios hechos")
            
    save_tasks(tasks)
                    
            
      
#Command executions

change_progress()