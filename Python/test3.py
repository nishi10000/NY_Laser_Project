import tkinter as tk#GUI
import os, tkinter.filedialog, tkinter.messagebox#GUI

import numpy as np#MovieToTxt
import cv2,socket,math#MovieToTxt

from my_singleton import MySingleton
from movie_to_txt import MovieToTxt

class GUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(u"MovieToTxt")
        self.root.geometry("300x200")
        self.text = tk.StringVar()
        self.text.set("Read File Path")
        self.label = tk.Label(self.root, textvariable=self.text,bg='LightSkyBlue', relief=tk.RIDGE, bd=2)

        self.button = tk.Button(self.root,
                                text="読み込みファイル",
                                command=self.changeText)
        self.button.pack(anchor="nw")
        self.label.pack(anchor="nw")

        self.text2 = tk.StringVar()
        self.text2.set("Write File Path")
        self.label2 = tk.Label(self.root, textvariable=self.text2,bg='LightSkyBlue', relief=tk.RIDGE, bd=2)
        self.button2 = tk.Button(self.root,
                                text="保存フォルダ",
                                command=self.changeText2)
        self.button2.pack(anchor="nw")
        self.label2.pack(anchor="nw")

        self.button3 = tk.Button(self.root,
                                text="変換",
                                command=self.Change)
        self.button3.pack(anchor="nw",pady=10)

        self.root.mainloop()

    def changeText(self):
        fTyp = [("","*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
        self.text.set(file) 
        my = MySingleton()#シングルトンによって、ファイルパスを共有させる。
        my.set_read_path(file)


    def changeText2(self):
        fTyp = [("text file","*.txt"),('Markdown', '*.md')]
        iDir = os.path.abspath(os.path.dirname(__file__))
        #file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
        file = tkinter.filedialog.asksaveasfilename(defaultextension='txt',initialdir = iDir,filetypes = fTyp,title = "Save as",)
        self.text2.set(file) 
        my = MySingleton()
        my.set_write_path(file)

    def Change(self):
        m_MovieToTxt=MovieToTxt()
        m_MovieToTxt.Output()
             

app=GUI()

