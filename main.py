import os
from datetime import date
from datetime import datetime
import json
from enum import Enum




#Constants
FILE_NAME = "tasks.json"
FORMAT_DATE = datetime.now().strftime('Dia: %d, Mes: %m, Año: %Y, A las %H:%M')
status_list = ["To do", "In-Progress", "Completed"]

#class to encapsulate functions to manipulate json
class TaskManager:
    #Constructor
    def __init__(self):
        self.tasks = self.load_tasks()
    
    #clear the terminal
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    #Load tasks
    def load_tasks(self):
        if not os.path.exists(FILE_NAME):
            print("File not found. Creating a new one!")
            return []
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
        
    #Save the task once made the changes
    def save_tasks(self):
        with open(FILE_NAME, "w") as file:
            json.dump(self.tasks, file, indent=4)
            
    #Create new task
    def add_task(self):
        self.clear_screen()
        new_task = {
                    "id" : self.__create_id(),
                    "Title": input("Input the title for the new task: \n"),
                    "description" : input("Input a description for the new task:\n"),
                    "status" : status_list[0],
                    "created_At" : FORMAT_DATE,
                    "updated_At" : FORMAT_DATE
            }
        self.tasks.append(new_task)
        self.save_tasks()
        print("Task saved")
        
    #verifies the input is a valid integer
    def get_int(self, prompt_valid, min_val = None, max_val = None):
        
        while True:
            
            #valids if it`s an int
            try:
                value =  int(input(prompt_valid))
            
                #checks if it`s min and max val are not None
                if min_val is not None and max_val is not None:
                    
                    #verify the int is in range
                    if not (min_val <= value <= max_val):
                        print(f"The number must be between or be {min_val} and/or {max_val} \n")
                        continue
                    
                self.clear_screen()
                return value
            
            except ValueError:
                print("Please input a valid number\n")
    
    #create id
    def __create_id(self):
        tasks = self.load_tasks()
        if not tasks:
            return 1
        
        return max(t["id"] for t in tasks) + 1

    #delete task
    def delete_task(self):
        #show the tasks to know the valid options to delete
        self.show_tasks(3)
        #we got the id to delete and we verify it is a valid int
        delete_id = self.get_int("type the id of the task to delete: \n")
        
        #we iterate tasks and compare with delete_id, if found returns True, not the value
        task = any((t for t in self.tasks if t["id"] == delete_id))
        
        #If the value was not found, stops the function
        if not task:
            print("No existe ninguna tarea con ese ID.\n")
            return
        
        sure = self.get_int("Are you sure you want to delete the task?\n"
                    "1. Yes, delete it\n"
                    "2. No, i changed my mind\n", 1, 2)
        
        if sure == 1:
            #if the value was found, we create a new list without the task to delete
            self.tasks = [t for t in self.tasks if t["id"] != delete_id]
            self.save_tasks()
            print("¡Task deleted!")
        else:
            print("changes was no made")

    #print tasks
    def print_tasks(self):
        for t in self.tasks:
            print(f"{t}\n")

    #update tasks
    def modify_task(self):
        self.show_tasks(3)
        upd_id = int(input("input the id the task you want to change: \n"))
        
        for task in self.tasks:
            if upd_id == task["id"]:
                task["Title"] = input("Input the new title: \n")
                task["description"] = input("Input the new description: \n")
                task["updated_At"] = FORMAT_DATE
                self.save_tasks()
                print("Task updated succesfully!\n")
                break
        else:
            print("ID not found. Changes not made!\n")

    #change progress of the task
    def update_progress(self):
        self.show_tasks(3)
        #ask an int and verifies it is
        changing_id = self.get_int("Input the task to modify\n")
        task = next((t for t in self.tasks if t["id"] == changing_id), None)
        
        if not task:
            print("No task was found with the ID you entered")
            return
        
        progress_num = self.get_int("Ingresa un numero para cambiar el progreso de la tarea:\n To do = 0\n In-Progress = 1\n Completed = 2\n")
        
        if 0 <= progress_num <= 2:
            task["status"] = status_list[progress_num]
            task["updated_At"] = FORMAT_DATE
            self.save_tasks()
            print("Progress updated sucessfully")
        else:
            print("Progress value not valid. Changes no made")

    #Filter all tasks
    def filter_tasks(self, status_task):
        state_value = state(status_task)
        
        if state_value == state.ALL:
            return self.tasks
        else:
            filtered_list = [t for t in self.tasks if t["status"] == status_list[state_value.value]]
            return filtered_list

    #Show tasks
    def show_tasks(self, state):
        
        filtered_tasks = self.filter_tasks(state)
        if not filtered_tasks:
            print("The list is empty. Nothing to show")
            return
        
        print(f"{"ID":<5} {"Title":<30} {"Status":<20}")
        print("_" * 60, "\n" )
        
        for tf in filtered_tasks:
            print(f"{tf["id"]:<5} {tf["Title"]:<30} {tf["status"]:<20} \n")

    #middle-function to handle fuction with parameter
    def show_tasks_handler(self):
        task_num = self.get_int(
            "type a number to show filtered tasks\n"
            "0. Show 'To-do' tasks\n"
            "1. Show 'In-progress tasks'\n"
            "2. Show 'Completed tasks'\n"
            "3. Show all tasks\n")
        
        self.show_tasks(task_num)
        
    

#list of values to filter list
class state(Enum):
    TODO = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    ALL = 3

manager = TaskManager()

#dict of functions
actions_tasks = {
    "1": manager.add_task,
    "2": manager.delete_task,
    "3": manager.modify_task,
    "4": manager.update_progress,
    "5": manager.show_tasks_handler
}    

#Interactive Menu
def main_menu():
    while True:
        print("_" * 60, "\n")
        print("Welcome to my CLI Task Tracker")
        print("_" * 60, "\n")
        print("1. Create a new task \n")
        print("2. Delete task\n")
        print("3. Modify task\n")
        print("4. Update progress of a task\n")
        print("5. Show tasks\n")
        print("9. Close\n")
        
        option = manager.get_int("type an option: ")
        if option == 9:
            print("Exiting...\n")
            break
        
        selected_action = actions_tasks.get(str(option))

        if selected_action:
            selected_action()
        else:
            "Option not valid. Try again\n"

        
        
        
#Command executions
main_menu()