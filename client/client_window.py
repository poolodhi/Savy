from Tkinter import *
from tkFileDialog import askopenfilename
import tkMessageBox
from socket import *
from PIL import Image, ImageTk
import thread
import threading
from recv_mp3 import *
from recv_mp4 import *
from recv_pdf import *
from recv_doc import *
import os

s=socket(AF_INET, SOCK_STREAM)
folderlist=[]




def p():
    print 'clicked'

def get_folderlist():
    global s
    a=[]
    print "connected..."
    l = 's'
    while l!='end\n':
        print "Receiving..."
        l = s.recv(1024)
        print l
        s.send('r')
        if(l!='end\n'):
            a.append(l)
    return a

def go_to_home():
    global w,s
    s.send('endd')
    print "go to home"
    print_folder_list(w)

def go_to_next(name,w):
    global s,folderlist,file_list
    s.send(name.rstrip("\n"))
    n=name.rstrip("\n")
    print 'sending data to server====>',name.rstrip("\n")
    
    if n.endswith('.mp3'):
        print "<====mp3===>"
        w.play_music()
        ##w.start_music()
        ##w.musicthread.join()
        ##print_folder_list(w)
    elif n.endswith('.mp4'):
        print"<=====mp4====>"
        vedio_recv(s)
        print_folder_list(w)
        ##print "file_list",file_list
        
    elif n.endswith('.pdf'):
        print "<====pdf===>"
        show_pdf(s,n)
        path="files\\"+n
        ##os.remove(path)
        print_folder_list(w)

    elif n.endswith('.docx') or n.endswith('.doc'):
        print "<====doc===>"
        show_doc(s,n)
        path="files\\"+n
        ##os.remove(path)
        print_folder_list(w)
    
    else:
        print "<====else part===>"
        folderlist=get_folderlist()
        print_folder_list(w)
    

def exit_server():
    global s,w
    s.send("exit")
    print "in exit function"
    s.close()
    w.root.destroy()
    exit(0)
    ##sys.exit()

def back_server(w):
    global s,folderlist
    print 'in back'
    s.send("back")
    folderlist=get_folderlist()
    print_folder_list(w)

def populate(frame):
    i=0
    j=0
    global folderlist,w
    B=[]
    for i in range(0,len(folderlist)-1):
        f=folderlist[i].rstrip("\n")
        if f.endswith('.mp3'):
            filename = 'mp3.jpg'
        elif f.endswith('.pdf'):
            filename = 'pdf.jpg'
        elif f.endswith('.doc') or f.endswith('.docx'):
            filename = 'doc.jpg'
        elif '.' in f:
            filename ='invalid.jpg'    
        else:
            filename = 'folder.jpg'
        
        image = Image.open(filename)
        image = image.resize((60, 60), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        b=Button(frame,text=folderlist[i],image=img,compound="top",command=lambda i=i: go_to_next(folderlist[i],w),
                 wraplength=70,activebackground='snow',bg='white')
        b.img = img
        B.append(b)
    for b in B:
        b.grid(row=i, column=j ,padx=20, pady=20)
        if(j<2):
            j+=1
        elif(j>=2):
            i+=1
            j=0

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

def print_folder_list(w):
        
    print folderlist
    print "in folder list function"

    w.f1.destroy()
    w.f1=Frame(w.root, bg = "#3F51B5",width=600,height=350)
    outerframe=Frame(w.f1,bg="#3F51B5",width=400,height=50)
    outerframe.pack_propagate(0)
    
    ff1=Frame(w.f1, background="#ffffff",height=500)
    canvas = Canvas(ff1, borderwidth=0, background="#ffffff")
    frame = Frame(canvas, background="#ffffff",height=350,width=600)
    vsb = Scrollbar(ff1, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((4,4), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
    populate(frame)

    back_b=Button(outerframe,text="back",command=lambda :back_server(w))
    exit_b=Button(outerframe,text="exit",command=exit_server)
    back_b.pack(side="left")
    exit_b.pack(side="right")
    
    ff1.pack()
    outerframe.pack(side="bottom")
    w.f1.pack_propagate(0)
    w.f1.pack()
        
        
    
def start_client_server(w,h,p):
    global s,folderlist
    port=int(p)    
    try:
        s.connect((h,port))
        error=0
    except:
        error=1
        print "error occured"
    if not error:
        s.send('l')
        print 'sending data to server'
        folderlist=get_folderlist()
        print_folder_list(w)
        

def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

class window:
    def __init__( self ):
        self.root = Tk()
        self.play=1
        self.pause=0
        self.stop=0
        
    def print_error(self):
        tkMessageBox.showinfo("Message", "Error in connection \nTRY LATER")

    def startserver(self):
        HOST=self.E1.get()
        ##PORT=self.E2.get()
        PORT=11004
        f=validate_ip(HOST)
        print f
        if(HOST!="" and f ):
            thread.start_new_thread(start_client_server,(self,HOST,PORT))
        else:
            tkMessageBox.showinfo("Message", "please enter a valid Ip address")
        
    def title_frame(self):
        self.titleframe= LabelFrame(self.root, text="",height=50, bg="navy",relief=FLAT)
        Label(self.titleframe,padx=10,text="SAVY",fg = "white",bg = "navy",font = "Times 30 bold").pack()
        self.titleframe.pack()

    def ip_window(self):
        global startserver
        self.root.wm_title("Savy")
        self.root.resizable( width=FALSE, height=FALSE)    
        self.root.geometry( '{}x{}'.format(650, 450))
        self.root.configure(bg="#3F51B5")
        self.title_frame()
        
        Frame(self.root,width=600,height=20,bg="#3F51B5").pack()
        
        self.f1=Frame(self.root, bg = "snow",width=500,height=150,bd=5,relief= GROOVE)
        self.sf1=Frame(self.f1, bg = "snow",width=500,height=50)
        self.sf2=Frame(self.f1,bg = "snow",width=400, height=50)
        self.sf3=Frame(self.f1,bg = "snow",width=400, height=50)
        
        self.sf1.pack_propagate(0)
        self.sf2.pack_propagate(0)
        self.sf3.pack_propagate(0)

        self.l1=Label(self.sf1 ,font = "Times 15 ", text="    Enter ip adderss    " , bg = "snow")
        self.l1.pack(side=LEFT)
        self.E1 = Entry(self.sf1, bd =5,width=40)
        self.E1.pack(side=LEFT)
##        self.l2=Label(self.sf2 ,font = "Times 15 ", text="    Enter port    " , bg = "snow")
##        self.l2.pack(side=LEFT)
##        self.E2 = Entry(self.sf2, bd =5,width=40	)
##        self.E2.pack(side=LEFT)
        self.b1=Button(self.sf3, font = "Times 13 ",text="  Connect  " , command=self.startserver)
        self.b1.pack()

        self.sf1.pack()
        self.sf2.pack()
        self.sf3.pack()

        self.f1.pack_propagate(0)
        self.f1.pack()
        
    def play_music(self):
        
        self.f1.destroy()
        self.f1=Frame(self.root, bg = "#3F51B5",width=600,height=350)



        self.imgframe=Frame(self.f1, bg = "snow",width=300,height=300)
        music_image = Image.open("music.jpg")
        music_image = music_image.resize((300,300), Image.ANTIALIAS)
        music_img = ImageTk.PhotoImage(music_image)
        
        self.l11=Label(self.imgframe,bg="snow",image=music_img)
        self.l11.music_img=music_img
        self.l11.pack()
        
        self.buttonframe=Frame(self.f1, bg = "snow",width=600,height=50)

        play_image = Image.open("play.jpg")
        play_image = play_image.resize((30, 30), Image.ANTIALIAS)
        play_img = ImageTk.PhotoImage(play_image)
        
        self.play_b=Button(self.buttonframe,text="", image=play_img,compound="top",bg="white",command=self.play_it,state=DISABLED)##play
        self.play_b.play_img=play_img

        pause_image = Image.open("pause.jpg")
        pause_image = pause_image.resize((30, 30), Image.ANTIALIAS)
        pause_img = ImageTk.PhotoImage(pause_image)
        
        self.pause_b=Button(self.buttonframe,text="",image=pause_img,compound="top",bg="white",command=self.pause_it)##pause
        self.pause_b.pause_img=pause_img

        stop_image = Image.open("stop.jpg")
        stop_image = stop_image.resize((30, 30), Image.ANTIALIAS)
        stop_img = ImageTk.PhotoImage(stop_image)
        
        self.stop_b=Button(self.buttonframe,text="",image=stop_img,compound="top",bg="white",command=self.stop_it)##stop
        self.stop_b.stop_img=stop_img

        
        home_image = Image.open("home.jpg")
        home_image = home_image.resize((30, 30), Image.ANTIALIAS)
        home_img = ImageTk.PhotoImage(home_image)
        
        self.home_b=Button(self.buttonframe,text="",image=home_img,compound="top",bg="white",command=go_to_home,state=DISABLED)##home
        self.home_b.home_img=home_img
        
        self.play_b.grid(row=0, column=1)
        self.pause_b.grid(row=0, column=2)
        self.stop_b.grid(row=0, column=3)
        self.home_b.grid(row=0, column=4)
        
        self.buttonframe.pack(side="bottom")
        self.imgframe.pack()
        self.f1.pack_propagate(0)
        self.f1.pack()

        self.musicthread=threading.Thread(target=play_mp3 ,args=(s,self))
        self.musicthread.start()
        
    def play_it(self):
        self.play_b.config(state=DISABLED)
        self.pause_b.config(state="normal")
        self.stop_b.config(state="normal")
        ##global s
        ##s.send('play')
        print "=======play it======"
        self.play=1
        self.pause=0
        print self.play
        
    def pause_it(self):
        self.pause_b.config(state=DISABLED)
        self.stop_b.config(state=DISABLED)
        self.play_b.config(state="normal")
        ##global s
        ##s.send('paus')
        print "=====pause it======"
        self.play=0
        self.pause=1
        print self.play
    def stop_it(self):
        print "=====stop it======"
        global s
        s.send('stop')
        self.stop=1
        print "go to home"
        print_folder_list(w)

    def change_button(self):
        self.home_b.config(state="normal")
        self.pause_b.config(state=DISABLED)
        self.play_b.config(state=DISABLED)
        self.stop_b.config(state=DISABLED)
        
    def createwindow(self):
        self.ip_window()
        self.root.mainloop()

w=window()
w.createwindow()
