import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

class Window:
    def __init__(self):
        self.DbFilePath = None
        self.DbFile = None
        self.Query = None
        
        self.DbFileIsOpen = False
        self.QueryTextIsDefault = True

        # Root
        self.root = Tk()
        self.root.title("SqlCat")

        # Menu
        self.MenuBar = Menu(self.root)
        self.MenuBarFile = Menu(self.MenuBar, tearoff=0)
        self.MenuBarFile.add_command(label="Open Database", command=self.DbOpenButtonOnClick)
        self.MenuBarFile.add_command(label="Close Database", command=self.DbCloseButtonOnClick)
        self.MenuBarFile.add_separator()
        self.MenuBarFile.add_command(label="Exit", command=self.root.quit)
        self.MenuBar.add_cascade(label="File", menu=self.MenuBarFile)
        self.root.config(menu=self.MenuBar)
        
        # ContentFrame
        self.ContentFrame = ttk.Frame(self.root, padding=(5,5,5,5))

        # Query Widgets.
        self.QueryText = Text(self.ContentFrame)
        self.QueryTextDefault()
        self.QueryText.bind('<Button-1>', self.QueryTextOnClick)
        
        self.QueryButton = ttk.Button(self.ContentFrame, text='Submit Query', command=self.QueryButtonOnClick)

        # Result Widgets.
        self.ResultText = Text(self.ContentFrame, relief="sunken")

        # Grid layouts.
        self.ContentFrame.grid(column=0, row=0, sticky=NSEW)
        self.QueryText.grid(column=0, row=0, sticky=NSEW)
        self.QueryButton.grid(column=0, row=1, sticky=E)
        self.ResultText.grid(column=0, row=2, sticky=NSEW)

        self.root.grid_columnconfigure(0, weight=1)
        self.ContentFrame.grid_columnconfigure(0, weight=1)
        self.ContentFrame.grid_rowconfigure(0, weight=1)
        self.ContentFrame.grid_rowconfigure(1, weight=1)
        self.ContentFrame.grid_rowconfigure(2, weight=1)

        # Set state to DbFileIsClosed
        self.StateDbClosed()
        
        # Mainloop.
        self.root.mainloop()
        
    def DbOpenButtonOnClick(self):
        self.DbFilePath = filedialog.askopenfilename()
        if self.DbFilePath:
            try:
                self.DbFile = sqlite3.connect(self.DbFilePath)
                self.StateDbOpen()
                self.ResultTextWrite("Connected to Database: %s " % self.DbFilePath)
            except sqlite3.Error:
                self.ResultTextWrite("Unable to connect to Database: %s " % self.DbFilePath)
            
    def DbCloseButtonOnClick(self):
        try:
            self.DbFile.close()
            self.StateDbClosed()
            self.QueryTextDefault()
        except sqlite3.Error:
            print('Uh oh')

    def QueryButtonOnClick(self):
        self.ResultTextDelete()
        Query = self.QueryText.get('1.0', END)
        c = self.DbFile.cursor()
        try:
            c.execute(Query)
            for t in c:
                self.ResultTextAppend(t)
                self.ResultTextAppend('\n')
            c.close()
        except sqlite3.Error as e:
            self.ResultTextWrite(e)
        except sqlite3.ProgrammingError as e:
            self.ResultTextWrite(e)
        
    def QueryTextOnClick(self, event):
        if self.DbFileIsOpen and self.QueryTextIsDefault:
            self.QueryTextDelete()
            self.QueryText['state'] = 'normal'
            self.QueryButton['state'] = 'normal'
            self.QueryTextIsDefault = False
        elif self.DbFileIsOpen:
            self.QueryText['state'] = 'normal'
            self.QueryButton['state'] = 'normal'

    def StateDbClosed(self):
        self.MenuBarFile.entryconfig(0, state=NORMAL)
        self.MenuBarFile.entryconfig(1, state=DISABLED)
        self.ResultTextWrite("Query Result...")
        self.QueryText['state'] = 'disabled'
        self.QueryButton['state'] = 'disabled'
        self.QueryTextIsDefault = True
        self.DbFileIsOpen = False
        
    def StateDbOpen(self):
        self.MenuBarFile.entryconfig(0, state=DISABLED)
        self.MenuBarFile.entryconfig(1, state=NORMAL)
        self.QueryButton['state'] = 'disabled'
        self.DbFileIsOpen = True

    def QueryTextDefault(self):
        self.QueryText['state'] = 'normal'
        self.QueryText.delete("1.0", END)
        self.QueryText.insert("1.0", "Type Query Here...")
        self.QueryText['state'] = 'disabled'

    def QueryTextDelete(self):
        self.QueryText['state'] = 'normal'
        self.QueryText.delete("1.0", END)
        self.QueryText['state'] = 'disabled'

    def ResultTextAppend(self, txt):
        self.ResultText['state'] = 'normal'
        self.ResultText.insert(END, txt)
        self.ResultText['state'] = 'disabled'

    def ResultTextDelete(self):
        self.ResultText['state'] = 'normal'
        self.ResultText.delete("1.0", END)
        self.ResultText['state'] = 'disabled'

    def ResultTextWrite(self, txt):
        self.ResultText['state'] = 'normal'
        self.ResultText.delete("1.0", END)
        self.ResultText.insert("1.0", txt)
        self.ResultText['state'] = 'disabled'

a = Window()
