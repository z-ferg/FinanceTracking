import tkinter as tk
from functools import partial
from pf_tkinter import *


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def instantiate_window():
    root = tk.Tk()
    root.title("Personal Finance Tracker")
    root.geometry("600x400")
    
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=4)
    
    # CONFIGURE THE FRAMES
    left_frame = tk.Frame(root, padx=5, pady=5)
    left_frame.grid(row=0, column=0)
    
    right_frame = tk.Frame(root)
    right_frame.grid(row=0, column=1)
    
    # CONFIGURE INTERACTIVE BUTTONS
    add_trans = tk.Button(left_frame, text="Add Transaction", command=partial(gui_add_transaction, right_frame))
    add_trans.grid(row=0, column=0, pady=10, padx=5)
    
    check_bal = tk.Button(left_frame, text="Check Balances", command=partial(gui_balances, right_frame))
    check_bal.grid(row=1, column=0, padx=10, pady=5)
    
    # CONFIGURE BOX FOR FUNCTION VISUALIZATION
    temp = tk.Text(right_frame, wrap="word", font=("Arial", 12))
    temp.grid(row=1, column=0, sticky="nsew", padx=5)
    
    return root


def gui_balances(frame):
    clear_frame(frame)
    #check_balances(frame)
    frame.pack()


def gui_add_transaction(frame):
    clear_frame(frame)
    #add_transaction(frame)
    frame.pack()


def main():
    root = instantiate_window()
    root.mainloop()

if __name__=="__main__":
    main()