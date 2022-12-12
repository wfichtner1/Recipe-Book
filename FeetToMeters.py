# https://tkdocs.com/tutorial/index.html
from tkinter import *
from tkinter import ttk

class FeetToMeters:

    def __init__(self, root):
        # root is main application window
        # set title of main application window
        root.title("Feet to Meters")

        # Create a content frame widget
        # configure to stretch to size of window
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # Create an Entry widget
        self.feet = StringVar()
        # add as child widget to mainframe widget
        feet_entry = ttk.Entry(mainframe, width=7, textvariable=self.feet)
        feet_entry.grid(column=2, row=1, sticky=(W, E))
        
        # Create additional widgets
        self.meters = StringVar()
        ttk.Label(mainframe, textvariable=self.meters).grid(column=2, row=2, sticky=(W, E))
        ttk.Button(mainframe, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky=W)

        ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
        ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
        ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

        # add padding to child widgets
        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        # set focus to feet_entry widget
        feet_entry.focus()

        # bind enter key to calculate method
        root.bind("<Return>", self.calculate)
        
    def calculate(self, *args):
        try:
            value = float(self.feet.get())
            self.meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
        except ValueError:
            pass
