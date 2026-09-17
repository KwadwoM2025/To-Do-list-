from pathlib import Path

import customtkinter as ctk

from recommender import Task_Recommendation_Engine
from tasks_data import Todo_Data
from graphics import TodoApp


def main() -> None:
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    data_file = Path("tasks.json")
    app = TodoApp(Todo_Data(data_file), Task_Recommendation_Engine())
    app.mainloop()


if __name__ == "__main__":
    main()