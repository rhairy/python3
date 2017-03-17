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

        # DbPath Widgets
        self.DbOpenButton = ttk.Button(self.ContentFrame, text='Open...', command=self.DbOpenButtonOnClick)

        # Query Widgets.
        self.QueryText = Text(self.ContentFrame, width=40, height=10)
        self.QueryText.insert('1.0', 'Type Query Here...')
        self.QueryText['state'] = 'disabled'
        self.QueryText.bind('<Button-1>', self.QueryTextOnClick)
        
        self.QueryButton = ttk.Button(self.ContentFrame, text='Submit Query', command=self.QueryButtonOnClick)
        self.QueryButton['state'] = 'disabled'

        # Result Widgets.
        self.ResultText = Text(self.ContentFrame, borderwidth=5, relief="sunken", width=40, height=10)
        self.ResultText.insert('1.0', 'Query Result...')
        self.ResultText['state'] = 'disabled'

        # Grid layouts.
        self.ContentFrame.grid(column=0, row=0)
        self.DbOpenButton.grid(column=0, row=0)
        self.QueryText.grid(column=0, row=1, columnspan=4, rowspan=2)
        self.QueryButton.grid(column=3, row=3)
        self.ResultText.grid(column=0, row=4, columnspan=4, rowspan=2)

        # Mainloop.
        self.root.mainloop()
        
    def DbOpenButtonOnClick(self):
        self.DbFilePath = filedialog.askopenfilename()
        self.DbFile = sqlite3.connect(self.DbFilePath)
        self.DbFileIsOpen = True
        self.DbOpenButton['state'] = 'disabled'

    def QueryButtonOnClick(self):
        self.QueryButton['state'] = 'disabled'
        self.ResultText['state'] = 'normal'
        self.ResultText.delete('1.0', END)
        Query = self.QueryText.get('1.0', END)
        c = self.DbFile.cursor()
        try:
            c.execute(Query)
            for t in c:
                self.ResultText.insert(END, t)
                self.ResultText.insert(END, '\n')
            c.close()
        except sqlite3.Error as e:
            self.ResultText.insert(END, e)
        self.ResultText['state'] = 'disabled'
        self.QueryButton['state'] = 'normal'
        
    def QueryTextOnClick(self, event):
        if self.DbFileIsOpen:
            self.QueryText['state'] = 'normal'
            self.QueryButton['state'] = 'normal'
        if self.QueryTextIsDefault and self.QueryText['state'] == 'normal':
            self.QueryText.delete('1.0', END)
            self.QueryTextIsDefault = False

a = Window()
