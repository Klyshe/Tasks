































import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер задач")
        self.root.geometry("500x450")
        self.root.resizable(True, True)
        self.style = ttk.Style()
        self.style.configure("Completed.TCheckbutton", foreground="gray")
        self.style.configure("Pending.TCheckbutton", foreground="black")
        self.tasks_file = "tasks.json"
        self.tasks = []
        self.load_tasks()
        self.create_widgets()
        
    def create_widgets(self):
        add_frame = ttk.Frame(self.root, padding="10")
        add_frame.pack(fill=tk.X)
        self.task_entry = ttk.Entry(add_frame, width=40)
        self.task_entry.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.X, expand=True)
        self.task_entry.bind("<Return>", lambda event: self.add_task())
        add_button = ttk.Button(add_frame, text="Добавить", command=self.add_task)
        add_button.pack(side=tk.RIGHT, padx=5)
        task_frame = ttk.Frame(self.root, padding="10")
        task_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(task_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas = tk.Canvas(task_frame, yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.canvas.yview)
        self.tasks_frame = ttk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.tasks_frame, anchor="nw")
        self.tasks_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.display_tasks()
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)
        delete_completed_button = ttk.Button(control_frame, text="Удалить выполненные", command=self.delete_completed_tasks)
        delete_completed_button.pack(side=tk.LEFT, padx=5)
        delete_all_button = ttk.Button(control_frame, text="Удалить все", command=self.delete_all_tasks)
        delete_all_button.pack(side=tk.RIGHT, padx=5)
    
    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event=None):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            task_id = 1
            if self.tasks:
                task_id = max(task["id"] for task in self.tasks) + 1
            self.tasks.append({"id": task_id, "text": task_text, "completed": False})
            self.task_entry.delete(0, tk.END)
            self.display_tasks()
            self.save_tasks()
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите текст задачи")
    
    def toggle_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                break
        self.display_tasks()
        self.save_tasks()
    
    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        self.display_tasks()
        self.save_tasks()
    
    def delete_completed_tasks(self):
        if any(task["completed"] for task in self.tasks):
            if messagebox.askyesno("Подтверждение", "Удалить все выполненные задачи?"):
                self.tasks = [task for task in self.tasks if not task["completed"]]
                self.display_tasks()
                self.save_tasks()
        else:
            messagebox.showinfo("Информация", "Нет выполненных задач для удаления")
    
    def delete_all_tasks(self):
        if self.tasks:
            if messagebox.askyesno("Подтверждение", "Удалить все задачи?"):
                self.tasks = []
                self.display_tasks()
                self.save_tasks()
        else:
            messagebox.showinfo("Информация", "Список задач пуст")
    
    def display_tasks(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
        if not self.tasks:
            no_tasks_label = ttk.Label(self.tasks_frame, text="Нет задач. Добавьте новую задачу выше.", padding="20")
            no_tasks_label.pack(pady=20)
            return
        for i, task in enumerate(self.tasks):
            task_frame = ttk.Frame(self.tasks_frame)
            task_frame.pack(fill=tk.X, pady=2)
            style = "Completed.TCheckbutton" if task["completed"] else "Pending.TCheckbutton"
            var = tk.BooleanVar(value=task["completed"])
            check = ttk.Checkbutton(task_frame, text=task["text"], variable=var, style=style, command=lambda t_id=task["id"]: self.toggle_task(t_id))
            check.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            delete_button = ttk.Button(task_frame, text="✕", width=3, command=lambda t_id=task["id"]: self.delete_task(t_id))
            delete_button.pack(side=tk.RIGHT, padx=5)
    
    def save_tasks(self):
        try:
            with open(self.tasks_file, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить задачи: {e}")
    
    def load_tasks(self):
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить задачи: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
