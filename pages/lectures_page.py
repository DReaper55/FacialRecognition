import tkinter as tk
from tkinter import ttk


def show_route3(self):
    self.main_frame.destroy()
    self.main_frame = tk.Frame(self, bg='white')
    self.main_frame.pack(side='right', fill='both', expand=True)
    label = ttk.Label(self.main_frame, text="This is Route 3")
    label.pack()
