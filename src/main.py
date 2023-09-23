import customtkinter as ctk
from CTkListbox import *
import json
import os


def save_to_list(content, file_path="./data.json"):
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f, indent=4)

    with open(file_path, "r+") as f:
        file_data = json.load(f)
        file_data.append(content)
        f.seek(0)
        json.dump(file_data, f, indent=4)


def delete_from_list(index, file_path="./data.json"):
    file_data = json.load(open(file_path))
    file_data.pop(index)
    with open(file_path, "w") as f:
        json.dump(file_data, f, indent=4)


class App(ctk.CTk):
    # Styling
    title_font = ("Arial", 55)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_content = ctk.StringVar()

        self.title("EchoRider Todo")
        self.geometry("500x500")
        # Title text
        self.program_label = ctk.CTkLabel(self, text="EchoRider Todo", font=self.title_font)
        self.program_label.pack(padx=0.5, pady=0.1, anchor=ctk.CENTER)
        # Task list
        self.task_listbox = CTkListbox(self)
        self.task_listbox.pack(fill="x")
        self.task_listbox.event_generate("<<ListboxSelect>>")

        # Task input bar
        self.input_bar = ctk.CTkEntry(self, textvariable=self.task_content)
        self.input_bar.pack(fill="x")
        self.input_bar.bind("<Return>", self.add_task)

        # Buttons
        # Add Button
        self.add_button = ctk.CTkButton(self, text="Add Task", command=self.add_task)
        self.add_button.pack(side="left", anchor="e", expand=True)
        # Delete Button
        self.delete_button = ctk.CTkButton(self, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side="left", anchor="w", expand=True)

        # # Show the contents of the task.
        # # This helps see the full task if it is too long to be displayed within the list box
        # self.task_label = ctk.CTkLabel(self)
        # self.task_label.pack(side="bottom", anchor="s")
        # self.bind("<<ListboxSelect>>", self.change_task_label)

    def get_selection(self):
        selection = self.task_listbox.curselection()
        return selection

    def delete_task(self):
        selected_task = self.get_selection()
        if selected_task is None:
            return
        self.task_listbox.delete(selected_task)
        delete_from_list(selected_task)

    def add_task(self, *input_type):
        content = self.task_content.get()
        self.task_listbox.insert("end", content)
        self.task_content.set("")
        save_to_list(content)

    # def change_task_label(self):
    #     selected_task = self.get_selection()
    #     content = selected_task.get()
    #     print("worked probably")
    #     self.task_label.config(text=content)

    def load_tasks(self, file_path="./data.json"):
        print("loading tasks")
        if os.path.exists(file_path):
            "path exists"
            with open(file_path, "r+") as f:
                file_data = json.load(f)
            for i in file_data:
                self.task_listbox.insert("end", i)


if __name__ == "__main__":
    app = App()
    app.load_tasks()
    app.mainloop()
