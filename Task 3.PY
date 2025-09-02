import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

DIRECTORY_STORAGE_FILE = 'personal_directory.json'

class PersonalDirectory:
    def __init__(self, root_gui):
        self.root_gui = root_gui
        root_gui.title("Personal Directory Organizer")
        root_gui.geometry("700x600")
        root_gui.resizable(True, True)

        self.directory_entries = self.retrieve_directory_data()

        self.entry_fields_panel = tk.Frame(root_gui, padx=10, pady=10)
        self.entry_fields_panel.pack(fill='x')

        tk.Label(self.entry_fields_panel, text="Full Name:").grid(row=0, column=0, sticky='w', pady=2)
        self.name_input_field = tk.Entry(self.entry_fields_panel, width=40)
        self.name_input_field.grid(row=0, column=1, sticky='ew', pady=2)

        tk.Label(self.entry_fields_panel, text="Contact Number:").grid(row=1, column=0, sticky='w', pady=2)
        self.phone_input_field = tk.Entry(self.entry_fields_panel, width=40)
        self.phone_input_field.grid(row=1, column=1, sticky='ew', pady=2)

        tk.Label(self.entry_fields_panel, text="Email Address:").grid(row=2, column=0, sticky='w', pady=2)
        self.email_input_field = tk.Entry(self.entry_fields_panel, width=40)
        self.email_input_field.grid(row=2, column=1, sticky='ew', pady=2)

        tk.Label(self.entry_fields_panel, text="Physical Address:").grid(row=3, column=0, sticky='w', pady=2)
        self.address_input_field = tk.Entry(self.entry_fields_panel, width=40)
        self.address_input_field.grid(row=3, column=1, sticky='ew', pady=2)

        self.control_buttons_panel = tk.Frame(root_gui, padx=10, pady=5)
        self.control_buttons_panel.pack(fill='x')

        self.add_entry_button = tk.Button(self.control_buttons_panel, text="Add New Entry", command=self.add_new_directory_entry)
        self.add_entry_button.pack(side=tk.LEFT, expand=True, fill='x', padx=(0, 5))

        self.update_entry_button = tk.Button(self.control_buttons_panel, text="Modify Selected", command=self.modify_selected_entry)
        self.update_entry_button.pack(side=tk.LEFT, expand=True, fill='x', padx=(0, 5))

        self.delete_entry_button = tk.Button(self.control_buttons_panel, text="Remove Selected", command=self.remove_selected_entry)
        self.delete_entry_button.pack(side=tk.LEFT, expand=True, fill='x')

        self.search_panel = tk.Frame(root_gui, padx=10, pady=5)
        self.search_panel.pack(fill='x')

        tk.Label(self.search_panel, text="Find By Name/Phone:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_query_field = tk.Entry(self.search_panel, width=30)
        self.search_query_field.pack(side=tk.LEFT, expand=True, fill='x')
        self.search_query_field.bind("<Return>", lambda event: self.execute_directory_search())

        self.initiate_search_button = tk.Button(self.search_panel, text="Search Directory", command=self.execute_directory_search)
        self.initiate_search_button.pack(side=tk.LEFT, padx=(5, 0))

        self.reset_search_button = tk.Button(self.search_panel, text="Show All Entries", command=self.clear_search_and_show_all)
        self.reset_search_button.pack(side=tk.LEFT, padx=(5, 0))

        self.display_list_panel = tk.Frame(root_gui, padx=10, pady=10)
        self.display_list_panel.pack(fill='both', expand=True)

        self.directory_listbox = tk.Listbox(self.display_list_panel, height=15, selectmode=tk.SINGLE)
        self.directory_listbox.pack(side=tk.LEFT, fill='both', expand=True)
        self.directory_listbox.bind("<<ListboxSelect>>", self.fill_fields_from_selection)

        self.directory_scrollbar = tk.Scrollbar(self.display_list_panel, orient="vertical", command=self.directory_listbox.yview)
        self.directory_scrollbar.pack(side=tk.RIGHT, fill='y')
        self.directory_listbox.config(yscrollcommand=self.directory_scrollbar.set)

        self.refresh_display_list()

    def retrieve_directory_data(self):
        if not os.path.exists(DIRECTORY_STORAGE_FILE) or os.stat(DIRECTORY_STORAGE_FILE).st_size == 0:
            return []
        try:
            with open(DIRECTORY_STORAGE_FILE, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            messagebox.showerror("Data Load Error", f"Encountered an issue loading directory entries: {e}. Initiating with an empty list.")
            return []

    def store_directory_data(self):
        try:
            with open(DIRECTORY_STORAGE_FILE, 'w') as f:
                json.dump(self.directory_entries, f, indent=4)
        except IOError as e:
            messagebox.showerror("Data Save Error", f"Unable to save directory entries to file: {e}")

    def refresh_display_list(self, entries_to_show=None):
        self.directory_listbox.delete(0, tk.END)
        display_collection = entries_to_show if entries_to_show is not None else self.directory_entries

        if not display_collection:
            self.directory_listbox.insert(tk.END, "No entries found. Add a new one or refine your search criteria!")
            return

        for i, entry in enumerate(display_collection, 1):
            display_line = f"{i}. Name: {entry.get('name', 'N/A')}, Phone: {entry.get('phone', 'N/A')}"
            self.directory_listbox.insert(tk.END, display_line)

    def reset_entry_fields(self):
        self.name_input_field.delete(0, tk.END)
        self.phone_input_field.delete(0, tk.END)
        self.email_input_field.delete(0, tk.END)
        self.address_input_field.delete(0, tk.END)

    def get_selected_entry_idx(self):
        selected_indices = self.directory_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Selection Required", "Please select an entry from the list to proceed with this action.")
            return -1
        return selected_indices[0]

    def fill_fields_from_selection(self, event=None):
        index = self.get_selected_entry_idx()
        if index != -1:
            search_text = self.search_query_field.get().strip().lower()
            
            if search_text:
                filtered_entries = [
                    c for c in self.directory_entries
                    if search_text in c.get('name', '').lower() or
                       search_text in c.get('phone', '').lower()
                ]
                if index < len(filtered_entries):
                    selected_entry = filtered_entries[index]
                else:
                    return
            else:
                selected_entry = self.directory_entries[index]

            self.reset_entry_fields()
            self.name_input_field.insert(0, selected_entry.get('name', ''))
            self.phone_input_field.insert(0, selected_entry.get('phone', ''))
            self.email_input_field.insert(0, selected_entry.get('email', ''))
            self.address_input_field.insert(0, selected_entry.get('address', ''))

    def add_new_directory_entry(self):
        name_val = self.name_input_field.get().strip()
        phone_val = self.phone_input_field.get().strip()
        email_val = self.email_input_field.get().strip()
        address_val = self.address_input_field.get().strip()

        if not name_val or not phone_val:
            messagebox.showwarning("Input Requirement", "Both 'Full Name' and 'Contact Number' are mandatory fields.")
            return

        new_entry = {
            'name': name_val,
            'phone': phone_val,
            'email': email_val,
            'address': address_val
        }
        self.directory_entries.append(new_entry)
        self.store_directory_data()
        self.refresh_display_list()
        self.reset_entry_fields()
        messagebox.showinfo("Entry Added", f"Directory entry for '{name_val}' successfully added.")

    def modify_selected_entry(self):
        index = self.get_selected_entry_idx()
        if index == -1:
            return

        search_text = self.search_query_field.get().strip().lower()
        if search_text:
            filtered_entries = [
                c for c in self.directory_entries
                if search_text in c.get('name', '').lower() or
                   search_text in c.get('phone', '').lower()
            ]
            if index < len(filtered_entries):
                original_entry_in_filtered_list = filtered_entries[index]
            else:
                messagebox.showerror("Update Error", "Selected entry not found in the current filtered view.")
                return
        else:
            original_entry_in_filtered_list = self.directory_entries[index]

        actual_idx_in_master_list = -1
        for i, entry in enumerate(self.directory_entries):
            if entry == original_entry_in_filtered_list:
                actual_idx_in_master_list = i
                break

        if actual_idx_in_master_list == -1:
            messagebox.showerror("Update Error", "Could not pinpoint the entry for modification.")
            return

        updated_name_val = self.name_input_field.get().strip()
        updated_phone_val = self.phone_input_field.get().strip()
        updated_email_val = self.email_input_field.get().strip()
        updated_address_val = self.address_input_field.get().strip()

        if not updated_name_val or not updated_phone_val:
            messagebox.showwarning("Input Requirement", "Both 'Full Name' and 'Contact Number' must be provided for updates.")
            return

        self.directory_entries[actual_idx_in_master_list] = {
            'name': updated_name_val,
            'phone': updated_phone_val,
            'email': updated_email_val,
            'address': updated_address_val
        }
        self.store_directory_data()
        self.refresh_display_list()
        self.reset_entry_fields()
        messagebox.showinfo("Entry Modified", f"Directory entry for '{updated_name_val}' successfully updated.")

    def remove_selected_entry(self):
        index = self.get_selected_entry_idx()
        if index == -1:
            return

        search_text = self.search_query_field.get().strip().lower()
        if search_text:
            filtered_entries = [
                c for c in self.directory_entries
                if search_text in c.get('name', '').lower() or
                   search_text in c.get('phone', '').lower()
            ]
            if index < len(filtered_entries):
                entry_to_delete_from_filtered = filtered_entries[index]
            else:
                messagebox.showerror("Deletion Error", "Selected entry not found in the current filtered view.")
                return
        else:
            entry_to_delete_from_filtered = self.directory_entries[index]

        actual_idx_in_master_list = -1
        for i, entry in enumerate(self.directory_entries):
            if entry == entry_to_delete_from_filtered:
                actual_idx_in_master_list = i
                break

        if actual_idx_in_master_list == -1:
            messagebox.showerror("Deletion Error", "Could not pinpoint the entry for removal.")
            return

        entry_name = self.directory_entries[actual_idx_in_master_list]['name']
        if messagebox.askyesno("Confirm Entry Removal", f"Are you certain you wish to permanently remove '{entry_name}' from your directory?"):
            del self.directory_entries[actual_idx_in_master_list]
            self.store_directory_data()
            self.refresh_display_list()
            self.reset_entry_fields()
            messagebox.showinfo("Entry Removed", f"'{entry_name}' has been successfully removed.")

    def execute_directory_search(self):
        query = self.search_query_field.get().strip().lower()
        if not query:
            self.refresh_display_list()
            return

        matching_entries = []
        for entry in self.directory_entries:
            if query in entry.get('name', '').lower() or \
               query in entry.get('phone', '').lower():
                matching_entries.append(entry)
        
        self.refresh_display_list(matching_entries)
        if not matching_entries:
            messagebox.showinfo("Search Result", "No entries found matching your search criteria.")

    def clear_search_and_show_all(self):
        self.search_query_field.delete(0, tk.END)
        self.refresh_display_list()

if __name__ == "__main__":
    root_instance = tk.Tk()
    application_instance = PersonalDirectory(root_instance)
    root_instance.mainloop()
