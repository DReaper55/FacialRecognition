import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

from database.student_db import getAllStudents, queryCount, insert, getOneStudent
from pages.home_page import show_home_page
from pages.courses_page import show_courses_page
from pages.lectures_page import show_lecture_page


def buildMenu(self):
    # Create the menu bar
    menu_bar = tk.Menu(self)
    self.config(menu=menu_bar)

    # Create the File menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Create the Add Music sub-menu
    file_menu.add_command(label="Add Music", command=add_music)


def add_music():
    print("Add music function called")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Attendance Management System")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        self.configure(bg='#f0f0f0')

        buildMenu(self)

        # Create the navigation frame
        self.nav_frame = tk.Frame(self, bg='#f0f0f0')
        self.nav_frame.pack(side='left', fill='y')

        # Create the main frame
        self.main_frame = tk.Frame(self, bg='#f0f0f0')
        self.main_frame.pack(side='right', fill='both', expand=True)

        # Create the navigation buttons
        self.home_page_btn = ttk.Button(self.nav_frame, text="Home Page", command=lambda: show_home_page(self))
        self.home_page_btn.pack(fill='x', pady=5, padx=12)
        self.courses_page_btn = ttk.Button(self.nav_frame, text="Courses", command=lambda: show_courses_page(self))
        self.courses_page_btn.pack(fill='x', pady=5, padx=12)
        self.lectures_page_btn = ttk.Button(self.nav_frame, text="Lectures", command=lambda: show_lecture_page(self))
        self.lectures_page_btn.pack(fill='x', pady=5, padx=12)

        # Go to first route
        self.home_page_btn.invoke()


if __name__ == '__main__':
    app = App()
    app.mainloop()
