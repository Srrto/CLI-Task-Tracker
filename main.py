import os
from datetime import date
from datetime import datetime
import json
from enum import Enum
import argparse

"""fix showing tasks, it gives an error when typing outside of State(Enum)"""


#clear the terminal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
#Validate input strings
def get_string(prompt):
    while True:
        text_val = input(prompt).strip()
        
        if not text_val:
            print("The text cannot be empty. Please type something\n")
            continue
        
        return text_val

#list of values to filter list
class State(Enum):
    TODO = "todo"
    PROGRESS = "progress"
    COMPLETED = "completed"
    ALL = "all"

#verifies the input is a valid integer
def get_int(prompt_valid, min_val = None, max_val = None):
    
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
                
            clear_screen()
            return value
        
        except ValueError:
            print("Please input a valid number\n")
    
def parse_state(status: str) -> State:
    
    try:
        return State(status.lower())
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{status}' is not a valid state, valid options are {[vo.value for vo in State]}")

#class to encapsulate functions to manipulate json
class TaskManager:
    #Constants
    FILE_NAME = "tasks.json"
    FORMAT_DATE = datetime.now().strftime('Dia: %d, Mes: %m, Año: %Y, A las %H:%M')
    
    #Constructor
    def __init__(self):
        
        self.tasks = self.load_tasks()
     
    #functions
        
    #Load tasks
    def load_tasks(self):
        if not os.path.exists(TaskManager.FILE_NAME):
            print("File not found. Creating a new one!")
            return []
        try:
            with open(TaskManager.FILE_NAME, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
        
    #Save the task once made the changes
    def save_tasks(self):
        with open(TaskManager.FILE_NAME, "w") as file:
            json.dump(self.tasks, file, indent=4)
            
    #Create new task
    def add_task(self, title = None, description = None):
        clear_screen()
        
        #validate if title was passed
        if title == None and description == None:
            title = get_string("Type the title for the task")
            description = get_string("Type a description for the task")
        
        new_task = {
                    "id" : self.__create_id(),
                    "Title": title,
                    "description" : description,
                    "status" : State.TODO,
                    "created_At" : self.FORMAT_DATE,
                    "updated_At" : self.FORMAT_DATE
            }
        self.tasks.append(new_task)
        self.save_tasks()
        print("Task saved")
        
    #create id
    def __create_id(self):
        tasks = self.load_tasks()
        if not tasks:
            return 1
        
        return max(t["id"] for t in tasks) + 1

    #delete task
    def delete_task(self, delete_id = None):
        
        if not delete_id:
            #show the tasks to know the valid options to delete
            self.show_tasks(State.ALL)
            #we got the id to delete and we verify it is a valid int
            delete_id = get_int("type the id of the task to delete: \n")
        
        #we iterate tasks and compare with delete_id, if found returns True, not the value
        task = any((t for t in self.tasks if t["id"] == delete_id))
        
        #If the value was not found, stops the function
        if not task:
            print("No existe ninguna tarea con ese ID.\n")
            return
        
        
        sure = get_int("Are you sure you want to delete the task?\n"
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
    def modify_task(self, modify_id = None, title = None, description = None):
        
        #get title and description if not provided by terminal
        if not title and not description and not modify_id:
            self.show_tasks(State.ALL)
            modify_id = get_int("Type the id of the task you want to modify\n")
            title = get_string("Type the new title\n")
            description = get_string("Type the new description\n")
        
        for task in self.tasks:
            if modify_id == task["id"]:
                task["Title"] = title
                task["description"] = description
                task["updated_At"] = self.FORMAT_DATE
                self.save_tasks()
                print("Task updated succesfully!\n")
                break
        else:
            print("ID not found. Changes not made!\n")

    #change progress of the task
    def update_progress(self, updating_id: int, progress: State):
        
        if not updating_id:   
            self.show_tasks(State.ALL)
            
            #ask an int and verifies it is
            updating_id = get_int("Input the task to modify\n")
            
        task = next((t for t in self.tasks if t["id"] == updating_id), None)
        
        #validate if there is a task with a valid updating_id
        if not task:
            print("No task was found with the ID you entered")
            return
        
        if progress is None:
            progress = get_int("Type the status of the task:\n todo\n inprogress\n completed\n")
            
        task["status"] = progress.name.upper()
        task["updated_At"] = TaskManager.FORMAT_DATE
        self.save_tasks()
        print("Progress updated sucessfully")
        

    #Filter all tasks
    def filter_tasks(self, status_task: State):
        
        
        if status_task == State.ALL:
            return self.tasks
        else:
            filtered_list = [t for t in self.tasks if t["status"] == status_task.name]
            return filtered_list

    #Show tasks
    def show_tasks(self, status_task: State):
        
        filtered_tasks = self.filter_tasks(status_task)
        if not filtered_tasks:
            print("The list is empty. Nothing to show")
            return
        
        print(f"{'ID':<5} {'Title':<30} {'Status':<20}")
        print("_" * 60, "\n" )
        
        for ft in filtered_tasks:
            print(f"{ft['id']:<5} {ft['Title']:<30} {ft['status']:<20} \n")

    #middle-function to handle show_tasks with parameter
    def show_tasks_handler(self):
        task_state = get_string(
            "type a word to show filtered tasks\n"
            "todo: Show 'To-do' tasks\n"
            "progress: Show 'In-progress tasks'\n"
            "completed: Show 'Completed tasks'\n"
            "all: Show all tasks\n")
        
        self.show_tasks(parse_state(task_state))


    
    

#towrite
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
def interactive_menu():
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
        
        option = get_int("type an option: ")
        if option == 9:
            print("Exiting...\n")
            break
        
        selected_action = actions_tasks.get(str(option))

        if selected_action:
            selected_action()
        else:
            "Option not valid. Try again\n"

def main():
    parser = argparse.ArgumentParser(description="CLI Task Tracker")
    subparsers = parser.add_subparsers(dest="command")
    
    #add task by terminal
    def add_task_command(args):
        manager.add_task(args.title, args.description)

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("title")
    add_parser.add_argument("description")
    add_parser.set_defaults(function = add_task_command)
    
    #delete task by terminal
    def delete_command(args):
        manager.delete_task(args.delete_id)
        
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("delete_id", type=int)
    delete_parser.set_defaults(function=delete_command)
    
    #print tasks by terminal
    def show_tasks_command(args):
        manager.show_tasks(args.filter)
        
    show_tasks_parser = subparsers.add_parser("show")
    show_tasks_parser.add_argument("filter", type=parse_state)
    show_tasks_parser.set_defaults(function=show_tasks_command)
    
    #modify task by terminal
    def modify_task_command(args):
        manager.modify_task(args.modify_id, args.new_title, args.new_description)
    
    modify_task_parser = subparsers.add_parser("modify")
    modify_task_parser.add_argument("modify_id", type=int)
    modify_task_parser.add_argument("new_title", type=str)
    modify_task_parser.add_argument("new_description", type=str)
    modify_task_parser.set_defaults(function=modify_task_command)
    
    #update status by terminal
    def update_task_command(args):
        manager.update_progress(args.id, args.progress)

    update_task_parse = subparsers.add_parser("update")
    update_task_parse.add_argument("id", type=int)
    update_task_parse.add_argument("status_task", type= parse_state)
    update_task_parse.set_defaults(function=update_task_command)
    
     
    
    args = parser.parse_args()
    if hasattr(args, "function"):
        args.function(args)
    else:
        parser.print_help()
        
if __name__ == "__main__":
    main()
    
    
interactive_menu()