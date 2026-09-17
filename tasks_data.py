#Use file handling and database tools like json, and path to handle the data input

import json #Saves and reloads tasks locally
from pathlib import Path #Safely handles the local-task data file path


from dataclasses import asdict 
from uuid import uuid4 #Generates unique ID's for tasks

from models import Todo_Items

class Todo_Data:
    def __init__(self, file_path:Path):
        self.file_path = Path(file_path)
        self.items = self._load()

    def _load(self) -> list[Todo_Items]:
        if not self.file_path.exists():
            return[]

#Load data from path using json. Files have an encoding of utf-8
#If there are any DecodeError, TypeErrors and KeyErrors, an empty list is returned
        try:
            data = json.loads(self.file_path.read_text(encoding="utf-8")) 
            return [Todo_Items(**item)for item in data]
        except (json.JSONDecodeError, TypeError, KeyError):
            return []


#Save data
    def _save(self) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        data = [asdict(item) for item in self.items]
        self.file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

#Add task
    def add(self, title: str) -> Todo_Items:
        title = title.strip()
        if not title:
            raise ValueError("Enter a task first")
        task = Todo_Items(id=str(uuid4()), title=title)
        self.items.insert(0, task)
        self._save()
        return task


    def find(self, task_id: str) -> Todo_Items:
        for task in self.items:
            if task.id == task_id:
                return task
            raise ValueError("Task not found")

    def toggle(self, task_id:str) -> None:
        task = self.find(task_id)
        task.completed = not task.completed
        self._save()

    def delete(self, task_id: str) -> None:
        self.items = [task for task in self.items if task.id != task_id]
        self._save()

    def all(self) -> list[Todo_Items]:
        return sorted(self.items, key=lambda task:(task.completed, task.title.lower()))

    
