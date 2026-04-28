import tkinter as tk
from tkinter import messagebox
import random
import json
import os

FILE_NAME = "history.json"

# Предопределённые задачи
tasks = [
    {"text": "Прочитать статью", "type": "Учёба"},
    {"text": "Сделать зарядку", "type": "Спорт"},
    {"text": "Ответить на письма", "type": "Работа"}
]

history = []

# Загрузка истории
def load_history():
    global history
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            history = json.load(f)
            update_history_list()

# Сохранение истории
def save_history():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

# Генерация задачи
def generate_task():
    selected_type = filter_var.get()

    filtered_tasks = tasks
    if selected_type != "Все":
        filtered_tasks = [t for t in tasks if t["type"] == selected_type]

    if not filtered_tasks:
        messagebox.showwarning("Ошибка", "Нет задач данного типа")
        return

    task = random.choice(filtered_tasks)
    result_label.config(text=f"{task['text']} ({task['type']})")

    history.append(task)
    update_history_list()
    save_history()

# Обновление списка истории
def update_history_list():
    history_listbox.delete(0, tk.END)
    for item in history:
        history_listbox.insert(tk.END, f"{item['text']} ({item['type']})")

# Добавление новой задачи
def add_task():
    text = task_entry.get().strip()
    task_type = type_var.get()

    if not text:
        messagebox.showerror("Ошибка", "Задача не может быть пустой")
        return

    tasks.append({"text": text, "type": task_type})
    task_entry.delete(0, tk.END)

# GUI
root = tk.Tk()
root.title("Random Task Generator")

# Фильтр
filter_var = tk.StringVar(value="Все")
tk.Label(root, text="Фильтр:").pack()
tk.OptionMenu(root, filter_var, "Все", "Учёба", "Спорт", "Работа").pack()

# Кнопка генерации
tk.Button(root, text="Сгенерировать задачу", command=generate_task).pack()

# Результат
result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack()

# История
tk.Label(root, text="История:").pack()
history_listbox = tk.Listbox(root, width=40)
history_listbox.pack()

# Добавление новой задачи
tk.Label(root, text="Новая задача:").pack()
task_entry = tk.Entry(root)
task_entry.pack()

type_var = tk.StringVar(value="Учёба")
tk.OptionMenu(root, type_var, "Учёба", "Спорт", "Работа").pack()

tk.Button(root, text="Добавить задачу", command=add_task).pack()

# Загрузка истории при старте
load_history()

root.mainloop()