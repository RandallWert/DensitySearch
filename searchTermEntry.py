from tkinter import *
from tkinter import ttk

def addToList(*args):
    global nextListLabelRow
    try:
        if len(newEntry.get()) > 0:
            searchTerms.append(newEntry.get())
            nextListLabelRow += 1
            ttk.Label(mainframe, text=newEntry.get()).grid(column=2, row=nextListLabelRow, sticky=W, padx=5, pady=5)
            term_entry.delete(0, END)
    except ValueError:
        pass

def commenceSearch():
    root.destroy()

def quitProgram():
    global quitRunning
    quitRunning = True
    root.destroy()
    
root = Tk()
root.title("Find density of examples in Google hits")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

newEntry = StringVar()

term_entry = ttk.Entry(mainframe, width=20, textvariable=newEntry)
term_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Button(mainframe, text="Add to list", command=addToList).grid(column=3, row=1, sticky=W)
ttk.Button(mainframe, text="Search", command=commenceSearch).grid(column=3, row=2, sticky=W)
ttk.Button(mainframe, text="Quit", command=quitProgram).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="Enter search term:").grid(column=1, row=1, sticky=E)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

term_entry.focus()
root.bind('<Return>', addToList)

searchTerms = []
nextListLabelRow = 1
quitRunning = False
root.mainloop()
