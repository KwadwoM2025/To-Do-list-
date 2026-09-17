import customtkinter as ctk

from recommender import Task_Recommendation_Engine
from tasks_data import Todo_Data


class TodoApp(ctk.CTk):
    def __init__(self, store: Todo_Data, recommender: Task_Recommendation_Engine):
        super().__init__()
        self.store = store
        self.recommender = recommender

        self.title("To-Do List")
        self.geometry("650x720")
        self.minsize(500, 560)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self._build_interface()
        self.refresh_tasks()

    def _build_interface(self) -> None:
        ctk.CTkLabel(
            self,
            text="To-Do List",
            font=ctk.CTkFont(size=32, weight="bold"),
        ).grid(row=0, column=0, padx=30, pady=(28, 4), sticky="w")

        self.summary = ctk.CTkLabel(self, text="")
        self.summary.grid(row=1, column=0, padx=30, pady=(0, 18), sticky="w")

        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.grid(row=2, column=0, padx=30, pady=(0, 12), sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="What needs to be done?",
            height=42,
        )
        self.entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.entry.bind("<Return>", lambda _: self.add_task())

        ctk.CTkButton(
            input_frame,
            text="Add task",
            width=110,
            height=42,
            command=self.add_task,
        ).grid(row=0, column=1)

        ai_frame = ctk.CTkFrame(self)
        ai_frame.grid(row=3, column=0, padx=30, pady=(0, 12), sticky="ew")
        ai_frame.grid_columnconfigure(0, weight=1)

        self.suggestion = ctk.CTkLabel(
            ai_frame,
            text="Ask AI for a task recommendation.",
            justify="left",
            wraplength=400,
        )
        self.suggestion.grid(row=0, column=0, padx=14, pady=12, sticky="w")

        ctk.CTkButton(
            ai_frame,
            text="Suggest task",
            command=self.get_suggestion,
        ).grid(row=0, column=1, padx=12, pady=12)

        self.message = ctk.CTkLabel(self, text="", text_color="#e35b5b")
        self.message.grid(row=4, column=0, padx=30, sticky="w")

        self.task_frame = ctk.CTkScrollableFrame(self, label_text="Tasks")
        self.task_frame.grid(row=5, column=0, padx=30, pady=(8, 28), sticky="nsew")

    def add_task(self) -> None:
        try:
            self.store.add(self.entry.get())
        except ValueError as error:
            self.message.configure(text=str(error))
            return

        self.entry.delete(0, "end")
        self.message.configure(text="")
        self.refresh_tasks()

    def get_suggestion(self) -> None:
        suggestion = self.recommender.suggest(
            self.store.all(),
            self.entry.get(),
        )
        self.suggestion.configure(text=f"AI suggestion: {suggestion}")
        self.entry.delete(0, "end")
        self.entry.insert(0, suggestion)

    def refresh_tasks(self) -> None:
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        tasks = self.store.all()
        remaining = sum(not task.completed for task in tasks)
        self.summary.configure(text=f"{remaining} active task(s)")

        if not tasks:
            ctk.CTkLabel(
                self.task_frame,
                text="No tasks yet. Add one above.",
            ).pack(pady=40)
            return

        for task in tasks:
            self._task_row(task)

    def _task_row(self, task) -> None:
        row = ctk.CTkFrame(self.task_frame)
        row.pack(fill="x", padx=5, pady=5)
        row.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            row,
            text="✓" if task.completed else "",
            width=32,
            command=lambda: self.toggle_task(task.id),
        ).grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkLabel(
            row,
            text=task.title,
            anchor="w",
            font=ctk.CTkFont(overstrike=task.completed),
        ).grid(row=0, column=1, sticky="ew")

        ctk.CTkButton(
            row,
            text="Delete",
            width=70,
            fg_color="#b84c4c",
            command=lambda: self.delete_task(task.id),
        ).grid(row=0, column=2, padx=10, pady=10)

    def toggle_task(self, task_id: str) -> None:
        self.store.toggle(task_id)
        self.refresh_tasks()

    def delete_task(self, task_id: str) -> None:
        self.store.delete(task_id)
        self.refresh_tasks()