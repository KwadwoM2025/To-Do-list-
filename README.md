# To-Do-list-
A to-do list app where a user can add, view, delete and complete tasks. 
Here's an overview of what each library does:
- `customtkinter` — Creates the native desktop graphical interface: windows, buttons, text fields, scrollable task list, and theme-aware widgets.

- `scikit-learn` — Provides the lightweight machine-learning recommendation feature. It compares task text using:
  - `TfidfVectorizer`: converts task words into numeric features.
  - `cosine_similarity`: finds which suggested task is most related to the user’s existing tasks.

- `json` — Built-in Python library that saves and reloads tasks locally as JSON data.

- `dataclasses` — Built-in Python feature used to define each task cleanly (`id`, `title`, `completed`).

- `pathlib` — Built-in library for safely handling the local task-data file path.

- `uuid` — Built-in library that generates unique IDs for tasks.

- `unittest` — Built-in Python testing framework used for test-driven development: adding, completing, deleting, and recommending tasks.

- `tempfile` — Built-in library used by tests to create temporary task files without affecting real user data.

- `sys` — Built-in library used to detect `--test`, so the same file can either launch the application or run its tests.
