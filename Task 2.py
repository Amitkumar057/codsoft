import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime

TASK_DATA_FILE = 'tasks_data.json'

class TaskOrganizerApp:
    def __init__(self, root_window):
        self.root_window = root_window
        root_window.title("Personal Task Manager")
        root_window.geometry("500x550")
        root_window.resizable(False, False)

        self.task_entries = self.retrieve_tasks_from_file()

        self.entry_section_frame = tk.Frame(root_window, padx=10, pady=10)
        self.entry_section_frame.pack(fill='x')

        self.task_description_label = tk.Label(self.entry_section_frame, text="Task Description:")
        self.task_description_label.pack(side=tk.LEFT, padx=(0, 5))

        self.task_description_entry = tk.Entry(self.entry_section_frame, width=40)
        self.task_description_entry.pack(side=tk.LEFT, expand=True, fill='x')
        self.task_description_entry.bind("<Return>", lambda event: self.add_new_task_entry())

        self.add_task_button = tk.Button(self.entry_section_frame, text="Add New Task", command=self.add_new_task_entry)
        self.add_task_button.pack(side=tk.RIGHT, padx=(5, 0))

        self.due_date_section_frame = tk.Frame(root_window, padx=10, pady=5)
        self.due_date_section_frame.pack(fill='x')

        self.due_date_input_label = tk.Label(self.due_date_section_frame, text="Target Completion Date (YYYY-MM-DD, optional):")
        self.due_date_input_label.pack(side=tk.LEFT, padx=(0, 5))

        self.due_date_input_entry = tk.Entry(self.due_date_section_frame, width=20)
        self.due_date_input_entry.pack(side=tk.LEFT, expand=False)

        self.task_display_frame = tk.Frame(root_window, padx=10, pady=10)
        self.task_display_frame.pack(fill='both', expand=True)

        self.task_display_listbox = tk.Listbox(self.task_display_frame, height=15, width=50, selectmode=tk.SINGLE)
        self.task_display_listbox.pack(side=tk.LEFT, fill='both', expand=True)

        self.list_scrollbar = tk.Scrollbar(self.task_display_frame, orient="vertical", command=self.task_display_listbox.yview)
        self.list_scrollbar.pack(side=tk.RIGHT, fill='y')
        self.task_display_listbox.config(yscrollcommand=self.list_scrollbar.set)

        self.action_buttons_frame = tk.Frame(root_window, padx=10, pady=10)
        self.action_buttons_frame.pack(fill='x')

        self.toggle_status_button = tk.Button(self.action_buttons_frame, text="Toggle Status", command=self.toggle_task_completion)
        self.toggle_status_button.pack(side=tk.LEFT, expand=True, fill='x', padx=(0, 5))

        self.edit_task_button = tk.Button(self.action_buttons_frame, text="Edit Task", command=self.modify_selected_task)
        self.edit_task_button.pack(side=tk.LEFT, expand=True, fill='x', padx=(0, 5))

        self.remove_task_button = tk.Button(self.action_buttons_frame, text="Remove Task", command=self.delete_selected_task)
        self.remove_task_button.pack(side=tk.LEFT, expand=True, fill='x')

        self.update_task_display()

    def retrieve_tasks_from_file(self):
        if not os.path.exists(TASK_DATA_FILE) or os.stat(TASK_DATA_FILE).st_size == 0:
            return []
        try:
            with open(TASK_DATA_FILE, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            messagebox.showerror("File Error", f"Problem loading tasks from file: {e}. Starting with an empty list.")
            return []

    def store_tasks_to_file(self):
        try:
            with open(TASK_DATA_FILE, 'w') as f:
                json.dump(self.task_entries, f, indent=4)
        except IOError as e:
            messagebox.showerror("File Error", f"Could not save tasks to file: {e}")

    def update_task_display(self):
        self.task_display_listbox.delete(0, tk.END)
        if not self.task_entries:
            self.task_display_listbox.insert(tk.END, "No tasks recorded yet. Use the input fields above to add one!")
            return

        for i, task_item in enumerate(self.task_entries, 1):
            status_indicator = "✓" if task_item['status'] == 'completed' else " "
            display_line = f"{i}. [{status_indicator}] {task_item['title']}"
            if task_item.get('due_date'):
                display_line += f" (Due: {task_item['due_date']})"
            self.task_display_listbox.insert(tk.END, display_line)
            if task_item['status'] == 'completed':
                self.task_display_listbox.itemconfig(tk.END, {'fg': 'gray'})

    def add_new_task_entry(self):
        task_title = self.task_description_entry.get().strip()
        due_date_string = self.due_date_input_entry.get().strip()
        
        if not task_title:
            messagebox.showwarning("Input Validation", "Task description cannot be empty.")
            return

        target_due_date = None
        if due_date_string:
            try:
                datetime.strptime(due_date_string, '%Y-%m-%d')
                target_due_date = due_date_string
            except ValueError:
                messagebox.showwarning("Input Validation", "Invalid date format for due date. Please use YYYY-MM-DD or leave blank.")
                return

        next_id = 1
        if self.task_entries:
            max_id = max(task['id'] for task in self.task_entries)
            next_id = max_id + 1

        new_task_item = {
            'id': next_id,
            'title': task_title,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'due_date': target_due_date
        }
        self.task_entries.append(new_task_item)
        self.store_tasks_to_file()
        self.update_task_display()
        self.task_description_entry.delete(0, tk.END)
        self.due_date_input_entry.delete(0, tk.END)
        messagebox.showinfo("Task Added", f"'{task_title}' successfully added to your list.")

    def get_current_selection_index(self):
        selected_indices = self.task_display_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Selection Required", "Please select a task from the list to perform this action.")
            return -1
        return selected_indices[0]

    def toggle_task_completion(self):
        index_to_modify = self.get_current_selection_index()
        if index_to_modify == -1:
            return

        selected_task = self.task_entries[index_to_modify]
        if selected_task['status'] == 'completed':
            selected_task['status'] = 'pending'
            messagebox.showinfo("Status Updated", f"Task '{selected_task['title']}' is now marked as pending.")
        else:
            selected_task['status'] = 'completed'
            messagebox.showinfo("Status Updated", f"Task '{selected_task['title']}' is now marked as completed.")
        
        self.store_tasks_to_file()
        self.update_task_display()

    def modify_selected_task(self):
        index_to_modify = self.get_current_selection_index()
        if index_to_modify == -1:
            return

        task_item_to_update = self.task_entries[index_to_modify]
        
        updated_title = simpledialog.askstring("Edit Task Description", "Enter the new description for the task:",
                                          initialvalue=task_item_to_update['title'])
        
        if updated_title is not None:
            updated_title = updated_title.strip()
            if updated_title:
                task_item_to_update['title'] = updated_title
                self.store_tasks_to_file()
                self.update_task_display()
                messagebox.showinfo("Update Successful", f"Task description changed to '{updated_title}'.")
            else:
                messagebox.showwarning("Input Validation", "Task description cannot be empty. Update cancelled.")

    def delete_selected_task(self):
        index_to_delete = self.get_current_selection_index()
        if index_to_delete == -1:
            return

        task_item_to_delete = self.task_entries[index_to_delete]
        if messagebox.askyesno("Confirm Task Removal", f"Are you sure you want to permanently remove '{task_item_to_delete['title']}'?"):
            del self.task_entries[index_to_delete]
            self.store_tasks_to_file()
            self.update_task_display()
            messagebox.showinfo("Task Removed", f"'{task_item_to_delete['title']}' has been deleted.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskOrganizerApp(root)
    root.mainloop()
