from tkinter import *
from tkinter import ttk

# Should I be using a global variable? Alternatives?
DbFilePath = ""

def OpenDbFile():
    global DbFilePath
    DbFilePath = filedialog.askopenfilename()
    
root = Tk()
root.title("SqlCat")

ContentFrame = ttk.Frame(root)

# DbPath Widgets
DbOpenButton = ttk.Button(ContentFrame, text='Open...', command=OpenDbFile)

# Query Widgets.
QueryText = Text(ContentFrame, width=40, height=10)
QueryText.insert('1.0', 'Type Query Here...')
QueryText['state'] = 'disabled'
QueryButton = ttk.Button(ContentFrame, text='Submit Query')

# Result Widgets.
ResultText = Text(ContentFrame, borderwidth=5, relief="sunken", width=40, height=10)
ResultText.insert('1.0', 'Query Result...')
ResultText['state'] = 'disabled'

# Grid layouts.
ContentFrame.grid(column=0, row=0)
DbOpenButton.grid(column=0, row=0)

QueryText.grid(column=0, row=1, columnspan=4, rowspan=2)
QueryButton.grid(column=3, row=3)
ResultText.grid(column=0, row=4, columnspan=4, rowspan=2)

# mainloop
root.mainloop()
