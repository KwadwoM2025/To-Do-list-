#Use the dataclasses built-in tool to cleanly define each task

from dataclasses import dataclass

@dataclass
class Todo_Items:
    id:str
    title:str
    completed:bool=False

#Set the identification and title of tasks an empty string.
#Set the completion of a task to False since no task has completed yet