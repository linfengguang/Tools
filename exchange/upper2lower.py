# -*- coding: utf-8 -*-

import wx
from tkinter import *
import tkinter.messagebox as messagebox

class ExchangeTools(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.creatWidgets()

    def creatWidgets(self):
        self.contentInput = Entry(self)
        self.contentInput.pack()
        self.alertButton = Button(self, text='大写转换', command=self.upper2lower)
        self.alertButton.pack()

    def upper2lower(self):
        content = self.contentInput.get()
        messagebox.showinfo('Message', '%s' % str(content).upper())

if __name__ == "__main__":
    app = ExchangeTools()
    app.master.title('ExchangeTools')
    app.mainloop()
