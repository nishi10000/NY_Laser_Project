import tkinter as tk
import os, tkinter.filedialog, tkinter.messagebox

class GUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(u"MovieToTxt")
        self.root.geometry("400x300")
        self.text = tk.StringVar()
        self.text.set("Read File Path")
        self.label = tk.Label(self.root, textvariable=self.text,bg='LightSkyBlue', relief=tk.RIDGE, bd=2)

        self.button = tk.Button(self.root,
                                text="Read",
                                command=self.changeText)
        self.button.pack(anchor="nw")
        self.label.pack(anchor="nw")

        self.text2 = tk.StringVar()
        self.text2.set("Write File Path")
        self.label2 = tk.Label(self.root, textvariable=self.text2,bg='LightSkyBlue', relief=tk.RIDGE, bd=2)
        self.button2 = tk.Button(self.root,
                                text="Write",
                                command=self.changeText2)
        self.button2.pack(anchor="nw")
        self.label2.pack(anchor="nw")

        self.root.mainloop()

    def changeText(self):
        fTyp = [("","*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
        self.text.set(file) 

    def changeText2(self):
        iDir = os.path.abspath(os.path.dirname(__file__))
        dir = tkinter.filedialog.askdirectory(initialdir = iDir)
        self.text2.set(dir)     

app=GUI()