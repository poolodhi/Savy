from Tkinter import *
from tkFileDialog import askopenfilename
import tkMessageBox
from folder_maker import *
##from start_server import *
from start_server1 import *
import threading


class window:
    def __init__( self ):
        self.root = Tk()
        self.l1text="Folder visible to client : NONE"
        self.progress_window()
        self.tp.withdraw()
        ##self.var1 = StringVar()##chaging path

    def percentage_send(self,pre):
        tkMessageBox.showinfo("Message", "Percentage send:\t"+pre)
        
    def getfolderpath( self ):    
        ##get folder path and store folder data in a txt file to be send to client
        global foldername
        foldername=self.E1.get()
        if(foldername==""):
            foldername="C:\Users\MR. V.P. SINGH\Music"
            self.l1text="Folder visible to client : MUSIC"
        else:
            self.l1text="Folder visible to client : "+foldername

        if(rightpath(foldername,'Main_folder_list')):
            tkMessageBox.showinfo("Message", "Folder selected sucessfully\n"+self.l1text)
            self.selectfolderframe.destroy()
            self.second_window()
        else:
            ##message dialogbox
            tkMessageBox.showerror("Warning", "No such file or directory\nPlease Enter Correct path")

    def title_frame(self):
        
        self.titleframe= LabelFrame(self.root, text="",width=990, height=100, bg="navy",relief=FLAT)
        Label(self.titleframe,padx=10,text="SAVY",fg = "white",bg = "navy",
		 font = "Times 60 bold").pack()
        self.titleframe.pack_propagate(0)
        self.titleframe.grid(row=0, column=0 ,columnspan=2 ,padx=5)
        
    def first_window(self):
        self.root.wm_title("Savy")
        self.root.resizable( width=FALSE, height=FALSE)    
        self.root.geometry( '{}x{}'.format(1000, 650))
        self.root.configure(bg="#3F51B5")
        self.title_frame()

        self.selectfolderframe = LabelFrame(self.root, text="",width=500, height=200, bg="snow" ,bd=5)
        self.selectfolderframe.pack_propagate(0)
        
        self.sf1=Frame(self.selectfolderframe, bg = "snow",width=700,height=50)
        self.sf2=Frame(self.selectfolderframe,bg = "snow",width=500, height=50)
        self.sf3=Frame(self.selectfolderframe,bg = "snow",width=500, height=50)
        self.sf1.pack_propagate(0)
        self.sf2.pack_propagate(0)
        self.sf3.pack_propagate(0)
        
        self.l2=Label(self.sf1 ,font = "Times 20 ", text="    SELECT THE FOLDER    " , bg = "papaya whip" ,fg="firebrick")
        ##self.l2.pack()
        self.l2.grid(row=0, column=0, pady=(20))
        self.l1=Label(self.sf2 ,font = "Times 15 ", text="    Enter the Folder    " , bg = "snow",fg="firebrick")
        self.l1.pack(side=LEFT)

        self.E1 = Entry(self.sf2, bd =5,width=40	)
        self.E1.pack(side=LEFT)
        ##self.sf1 = LabelFrame(self.root, text="",width=50, bg="snow")
        
        self.b1=Button(self.sf3, font = "Times 13 ",text="  OK  " , command=self.getfolderpath)
        ##self.b1.pack()
        self.b1.grid(row=2, column=0, pady=(10))

        self.sf1.pack()
        self.sf2.pack()
        self.sf3.pack()

        
        ###self.sf1.pack()
        self.selectfolderframe.grid(row=1, column=0 ,padx=220, pady=20)
        self.root.mainloop()

        
    def second_window(self):
        self.setupframe = LabelFrame(self.root,font = "Times 20 bold ", text="Setup Server",width=400, height=200,
                                     fg="saddle brown" ,bg="Blanched almond",relief=FLAT)

        self.clientframe = LabelFrame(self.root,font = "Times 20 bold ", text="Clients Connected",width=500, height=500,
                                      fg="saddle brown" ,bg="Blanched almond",relief=FLAT)
        self.ff2=Frame(self.clientframe,background="snow",width=500, height=500)
        self.clientframe2 = Frame(self.ff2,width=450, height=450, bg="snow")
        
        self.extraframe = LabelFrame(self.root,font = "Times 20 bold ", text="Extra info",width=400, height=250,
                                     fg="saddle brown" ,bg="Blanched almond",relief=FLAT)
        self.ff3=Frame(self.extraframe,background="snow",width=400, height=250)
        self.extraframe2 = Frame(self.ff3,width=400, height=250, bg="snow") 

        self.setupframe.pack_propagate(0)
        self.clientframe.pack_propagate(0)
        self.extraframe.pack_propagate(0)
        self.clientframe2.pack_propagate(0)
        self.extraframe2.pack_propagate(0)
        self.ff2.pack_propagate(0)
        self.ff3.pack_propagate(1)

        self.clientframe2.pack()
        self.extraframe2.pack()
        self.ff2.pack()
        self.ff3.pack()

        self.setupframe.grid(row=1, column=0 ,padx=20, pady=20)
        self.extraframe.grid(row=2, column=0, padx=8)
        self.clientframe.grid(row=1, column=1 ,rowspan=2,sticky='nw',padx=20, pady=20)

        self.setup_frame()

    def setup_frame(self):
        self.ff1=Frame(self.setupframe,background="snow",width=400, height=150)
        self.ff1.pack_propagate(0)
        
        self.f1=Frame(self.ff1,background="snow",width=400, height=150)
        self.f2=Frame(self.ff1,bg = "snow",width=400, height=250)
        self.f3=Frame(self.ff1,bg = "snow",width=400, height=250)
        self.f4=Frame(self.ff1,bg = "snow",width=400, height=250)

        self.l2=Label(self.f1 ,text=self.l1text, bg = "snow",wraplength=350 ,fg="firebrick")
        ##self.l2.pack(side=LEFT)
        self.l2.grid(pady=5)
        
        self.b2 = Button(self.f2 ,text=" Start Server " , command=self.disable_startsrver_button,fg="midnight blue")
        ##self.b2.pack()
        self.b2.grid(pady=5)
        self.l3=Label(self.f3 , font=('helvetica',10,'bold'),text="" , bg = "snow",fg="firebrick4")
        ##self.l3.pack()
        self.l3.grid(pady=5)
        self.b4 = Button(self.f4 ,text=" Progress Info " , command=self.progress_window_show,fg="midnight blue")
        self.b4.grid(pady=5)

        
        self.f1.pack()
        self.f2.pack()
        self.f3.pack()
        self.f4.pack()


        self.ff1.grid(pady=(10))
    def disable_startsrver_button(self):
        self.b2.config(state=DISABLED)
        self.l3.config(text="Server is running")
        global foldername
        startserver(self,foldername)

    def progress_window(self):
        self.tp=Toplevel(self.root)
        self.tp.wm_title("Savy Progress Info of Client")
        self.tp.resizable( width=FALSE, height=FALSE)    
        self.tp.geometry( '{}x{}'.format(600, 500))
        self.tp.configure(bg="#3F51B5")
        self.frame_tp3=Frame(self.tp,height=10,bg="#3F51B5")
        self.frame_tp3.pack()
        self.title_tp=Label(self.tp,text="Progress of clients",font = "Times 20 ",bg="blue4",fg="white",padx=10,pady=10)
        self.title_tp.pack()
        
        self.frame_tp1=Frame(self.tp,height=20,bg="#3F51B5")
        self.frame_tp1.pack()
        self.frame_tp=Frame(self.tp,width=500,height=400)
        self.frame_tp.pack()

        self.tp.protocol("WM_DELETE_WINDOW", self.tp.withdraw)

    def progress_window_show(self):
        self.tp.update()
        self.tp.deiconify()
        
    def createwindow(self):
        self.first_window()

        
