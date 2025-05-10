import tkinter as tk
from tkinter import filedialog

def choose_folder()->str:
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost',1)
    folder = filedialog.askdirectory(master=root)
    return folder