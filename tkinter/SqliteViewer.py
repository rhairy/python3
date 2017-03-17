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
        
        self.root = Tk()
        self.root.title("SqlCat")

        self.ContentFrame = ttk.Frame(self.root)

        # DbCloseButton
        self.DbCloseButton = ttk.Button(self.ContentFrame, text='Close', command=self.DbCloseButtonOnClick)
        
        # DbOpenButton
        self.DbOpenButton = ttk.Button(self.ContentFrame, text='Open...', command=self.DbOpenButtonOnClick)

        # Query Widgets.
        self.QueryText = Text(self.ContentFrame, width=40, height=10)
        self.QueryTextDefault()
        self.QueryText.bind('<Button-1>', self.QueryTextOnClick)
        
        self.QueryButton = ttk.Button(self.ContentFrame, text='Submit Query', command=self.QueryButtonOnClick)

        # Result Widgets.
        self.ResultText = Text(self.ContentFrame, borderwidth=5, relief="sunken", width=40, height=10)

        # Grid layouts.
        self.ContentFrame.grid(column=0, row=0)
        self.DbOpenButton.grid(column=0, row=0)
        self.DbCloseButton.grid(column=2, row=0)
        self.QueryText.grid(column=0, row=1, columnspan=4, rowspan=2)
        self.QueryButton.grid(column=3, row=3)
        self.ResultText.grid(column=0, row=4, columnspan=4, rowspan=2)

        # Set state to DbFileIsClosed
        self.StateDbClosed()
        
        # Mainloop.
        self.root.mainloop()
        
    def DbOpenButtonOnClick(self):
        self.DbFilePath = filedialog.askopenfilename()
        try:
            self.DbFile = sqlite3.connect(self.DbFilePath)
            self.StateDbOpen()
            self.ResultTextWrite("Connected to Database: %s " % self.DbFilePath)
        except sqlite3.Error:
            print("Uh oh")
            
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
        self.DbOpenButton['state'] = 'normal'
        self.DbCloseButton['state'] = 'disabled'
        self.ResultTextWrite("Query Result...")
        self.QueryText['state'] = 'disabled'
        self.QueryButton['state'] = 'disabled'
        self.QueryTextIsDefault = True
        self.DbFileIsOpen = False
        
    def StateDbOpen(self):
        self.DbOpenButton['state'] = 'disabled'
        self.DbCloseButton['state'] = 'normal'
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
