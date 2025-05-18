import random
from tkinter import *
from tkinter import ttk



class ConversionProgram:

    def __init__(self, root):
        self.toMeters = True
        root.title("How good are you at conversion?")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.feet = StringVar()
        self.feet_entry = ttk.Entry(mainframe, width=7, textvariable=self.feet)
        self.feet_entry.grid(column=2, row=1, sticky=(W, E))

        self.meters = StringVar()
        self.meters_entry = ttk.Entry(mainframe, width=7, textvariable=self.meters)
        self.meters_entry.grid(column=2, row=2, sticky=(W, E))
        self.meters_entry.config(state='disabled')

        ttk.Button(mainframe, text="Check Answer", command=self.calculate).grid(column=4, row=2, sticky=W)
        ttk.Button(mainframe, text="Invert", command=self.invert).grid(column=4, row=3, sticky=W)

        ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
        ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
        ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        self.feet_entry.focus()
        root.bind("<Return>", self.calculate)

    def calculate(self,*args):
        toMeters = self.toMeters
        try:
            # Get the values from the input fields
            if not toMeters:
                value = float(self.meters.get())
                self.feet.set(int(value * 10000.0 - 0.5)/(0.3048 * 10000.0))
            else:
                value = float(self.feet.get())
                self.meters.set(int(3.28084 * value * 10000.0 + 0.5)/10000.0)
        except ValueError:
            pass


    def invert(self,*args):
        toMeters = self.toMeters
        try:
            print("TO METERS: " + str(toMeters))
            if toMeters:
                # DISABLE FEET
                print("DISABLE FEET")
                self.feet_entry.config(state='disabled')
                self.meters_entry.config(state='normal')
            else:
                # DISABLE METERS
                print("DISABLE METERS")
                self.meters_entry.config(state='disabled')
                self.feet_entry.config(state='normal')
            self.toMeters = not toMeters
        except ValueError:
            pass





root = Tk()
ConversionProgram(root)
root.mainloop()