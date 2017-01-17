from socket import *
from Tkinter import *
import time
import threading
import os, sys
from Queue import Queue


from communicate import *
from folder_maker import *
from thread_index import *
##from extra_info import *


s = threading.Semaphore(1)
active = threading.Semaphore(1)
s1 = threading.Semaphore(1)
client_ref=[]

    
def printname(t,w):
    global active_extrainfo
    temp=[]
    print "going into extra info function:",t
    for a in client_ref:
        if(t==a[1]):
            ##print a
            ref=a
            break
    for a in thread:
        if(t==a[1]):
            ##print a
            threadcall=a[0]
            break
    with active:
        for a in active_extrainfo:
            if(t[0]==a[1][0] and t[1]==a[1][1]):
                ##print a
                ##active_extrainfo.remove(a)
                temp.append((1,t))
                ##print "if:",active_extrainfo,"temp",temp
            else:
                ##active_extrainfo.remove(a)
                temp.append((0,a[1]))
                ##print "else:",active_extrainfo,"temp",temp
        active_extrainfo=temp
        print "final======>",active_extrainfo
        
    if(ref[0].sending==0):    
        threadcall.work_in_extra_info(w,ref[0],ref[1],"No data sending")
    else:
        threadcall.work_in_extra_info(w,ref[0],ref[1],"check")
        

def client_list(w):
        global clientlist
        ##w.ff2.destroy()
        ##w.ff2=Frame(w.clientframe,background="snow",width=500, height=500)
        w.clientframe2.destroy()
        w.clientframe2=Frame(w.ff2,width=500, height=500, bg="snow" )
        ##for c in clientlist:
        ##        Button(w.clientframe2,text=c,command=lambda:printname(c,w)).pack()
        for i in range(0,len(clientlist)):
            x=str(i+1)
            Button(w.clientframe2,fg="midnight blue",font="Verdana 10",padx=30, pady=5,bg="seashell2"
                   ,text="Client "+x+"::: "+clientlist[i][0]+"\t"+str(clientlist[i][1]),command=lambda i=i: printname(clientlist[i],w)).pack()
        w.clientframe2.pack_propagate(0)
        w.clientframe2.pack()
        ##w.ff2.pack()





def fun(w,conn,addr,path):
    ##print t
    client=communicate(conn,addr,path)
    for a in thread:
        if(a[1]==addr):
            ##print a
            threadcall=a[0]
            break
    with s:
            print clientlist
            client_list(w)
            client_ref.append((client,addr))
    
    device_type=client.recv_data().rstrip("\n")        
    client.set_type(device_type)##setting type
    if client.type=='m':
        client.c.send(str(addr[1])+"\n")
    client.send_folder_list("Main_folder_list.txt")
    print "main folder send successfully............"

    pathlen = len(path)

    e=""
    while True:
        print 'in loop'
        d=client.recv_data()
        d=d.rstrip('\n')
        print 'getting data',d
        if d=="exit":
            ##w.var1=set("Client get disconnected")
            try:
                threadcall.work_in_extra_info(w,client,addr,"CLIENT GET DISCONNECTED")
                clientfolder="folder"+client.retrun_clientname()+'.txt'
                os.remove(clientfolder)
                break
            except:
                print "error occur while exiting"
                break
        elif d=='main':
            client.send_folder_list("Main_folder_list.txt")
            print "main folder send successfully............"
        elif d.endswith('.mp3'):
            print "in mp3===>filename"+d
            threadcall.work_in_extra_info(w,client,addr,"Streaming File:\t"+d)
            client.send_mp3(d)
            print "back to main"
        elif d.endswith('.mp4'):
            threadcall.work_in_extra_info(w,client,addr,"Streaming File:\t"+d)
            client.send_mp4(d)
            print "in mp4===>filename"+d
        elif d.endswith('.pdf'):
            threadcall.work_in_extra_info(w,client,addr,"Sending File:\t"+d)
            client.send_pdf(d)
            print "in PDF===>filename"+d
        elif d.endswith('.doc') or d.endswith('.docx'):
            threadcall.work_in_extra_info(w,client,addr,"Sending File:\t"+d)
            client.send_doc(d)
            print "in Doc===>filename"+d
        elif d=="back":
            clientfolder="folder"+client.retrun_clientname()
            f=client.return_path()
            k=f.rindex('\\')
            f=f[:k]
            print f
            if(len(f)<pathlen):
                f=path
                rightpath(f,clientfolder)
                client.set_path(f)
                ##w.var1=set("Currently :"+client.return_path())
                threadcall.work_in_extra_info(w,client,addr,"No data sending")
                print "Folder selected sucessfully"
                client.send_folder_list(clientfolder+".txt")
                
            elif(rightpath(f,clientfolder)):
                client.set_path(f)
                ##w.var1=set("Currently :"+client.return_path())
                threadcall.work_in_extra_info(w,client,addr,"No data sending")
                print "Folder selected sucessfully"
                client.send_folder_list(clientfolder+".txt")
                
            else:
                print "No such file or directory"
            print "back"
        elif d=="same":
            clientfolder="folder"+client.retrun_clientname()
            f=client.return_path()
            print f
            if(rightpath(f,clientfolder)):
                client.set_path(f)
                ##w.var1=set("Currently :"+client.return_path())
                threadcall.work_in_extra_info(w,client,addr,"No data sending")
                print "Folder selected sucessfully"
                client.send_folder_list(clientfolder+".txt")
        
        elif d=="":
            ##pass
            try:
                clientfolder="folder"+client.retrun_clientname()+'.txt'
                os.remove(clientfolder)
                break
            except:
                break
        else:
            
            clientfolder="folder"+client.retrun_clientname()
            f=client.return_path()+"\\"+d
            print f
            if(rightpath(f,clientfolder)):
                client.set_path(f)
                ##w.var1=set("Currently :"+client.return_path())
                threadcall.work_in_extra_info(w,client,addr,"No data sending")
                print "Folder selected sucessfully"
                client.send_folder_list(clientfolder+".txt")
            else:
                print "No such file or directory"
            ##client.send_folder_list(clientfloder)
            ##
            ##client.send_folder_list(d)
            
########remove it later############
##    time.sleep(10)
#######################
##    with s:
##        client_ref.remove((client,addr))
##        print clientlist
##        client_list(w)
    with active:
        for a in active_extrainfo:
            if(a[1]==addr):
                active_extrainfo.remove(a)
    client.close()
    print "thread closed"
    with s:
            client_ref.remove((client,addr))
            print clientlist
            client_list(w)
    ##thread.exit()


thread=[]
class MyThread(threading.Thread):
    ##def __init__(self,args=(), kwargs=None):
    ##    threading.Thread.__init__(self,args=(), kwargs=None)

    def run(self):
        self.name=threading.currentThread().getName()
        print threading.currentThread().getName()
        if sys.version_info[0] == 2:
            self._Thread__target(*self._Thread__args)
        else: # assuming v3
            self._target(*self._args)

    def work_in_extra_info(self,w,r,a,string_print):
        ##global e_t
        global var1
        ref=r
        ##print a
        

        for a1 in active_extrainfo:
            if a1[0]==1 and a1[1]==a:
                print a1
                addr=a
                v="Currently :"+ref.return_path()
                w.extraframe2.destroy()
                w.ff3.destroy()
                w.ff3=Frame(w.extraframe,background="snow",width=400, height=250)
                w.extraframe2=Frame(w.ff3,width=500, height=500, bg="snow" )
                Label(w.ff3,text="IP:"+addr[0]+"\tPORT:"+str(addr[1]),bg="snow",fg="HotPink4",font="Helvetica 10 bold italic",pady=10,padx=10).pack()
                ##Label(w.ff3,text=self.name,bg="snow",fg="HotPink4",font="Helvetica 10 bold italic").pack()
                Label(w.ff3,text=v,bg="snow",wraplength=350,fg="HotPink4",pady=10,padx=10).pack()

                if(string_print=="check"):
                    Label(w.ff3,text=r.string_print,bg="snow",wraplength=350,fg="HotPink4",pady=10,padx=10).pack()
                else:
                    Label(w.ff3,text=string_print,bg="snow",wraplength=350,fg="HotPink4",pady=10,padx=10).pack()


                if(string_print!="No data sending" or string_print!="CLIENT GET DISCONNECTED"):
                    Button(w.ff3,text="Amount Send",command=lambda : w.percentage_send(str(r.percentage))).pack()
                

                
                w.ff3.pack_propagate(0)
                w.extraframe2.pack_propagate(0)
                w.extraframe2.pack()
                w.ff3.pack()
                ##break





def fun1(w,path):
    SERVER_PORT=11004
    soc = socket(AF_INET, SOCK_STREAM)
    soc.bind(('', SERVER_PORT))
    soc.listen(5)
    print gethostbyname(gethostname())
    ##Label(w.f3 , text=gethostbyname(gethostname()), bg = "snow",wraplength=350).pack()

    while True:
        conn,addr=soc.accept()
        clientlist.append(addr)
        ##with active:
        active_extrainfo.append((0,addr))
        t=MyThread(target=fun,args=(w,conn,addr,path))
        thread.append((t,addr))## thread,address
        with all_false_lock:
            thread_list1.append({'thread':t,'getlock':False,'ipaddr':addr[0],'port':addr[1],'conn_obj':conn,'sending':False,'pause':False})##storing data for round robin list
        t.start()

    soc.close()
    
def fun2(w):
    print "in fun2"
    while True:
        w.frame_tp.destroy()
        ##w.progress_window()
        w.frame_tp=Frame(w.tp,width=500,height=400)
        w.frame_tp2=Frame(w.frame_tp,width=500,height=400)

        Label(w.frame_tp2,text="SNO",bg="royal blue",fg="white",font="Helvetica 10 bold italic",padx=10,pady=10).grid(row=0, column=0, pady=(20),padx=(20))
        Label(w.frame_tp2,text="CLIENT IP",bg="royal blue",fg="white",font="Helvetica 10 bold italic",padx=10,pady=10).grid(row=0, column=1, pady=(20),padx=(20))
        Label(w.frame_tp2,text="PORT",bg="royal blue",fg="white",font="Helvetica 10 bold italic",padx=10,pady=10).grid(row=0, column=2, pady=(20),padx=(20))
        Label(w.frame_tp2,text="PROGRESS",bg="royal blue",fg="white",font="Helvetica 10 bold italic",padx=10,pady=10).grid(row=0, column=3, pady=(20),padx=(20))
        ##w.frame_tp.pack()
        for i in range(0,len(clientlist)):
                sno=str(i+1)    
                for a in client_ref:
                    if(clientlist[i]==a[1]):
                        ref=a[0]
                        Label(w.frame_tp2,text=sno,font="Verdana 10").grid(row=int(sno), column=0, pady=(5))
                        Label(w.frame_tp2,text=str(clientlist[i][0]),font="Verdana 10").grid(row=int(sno), column=1, pady=(5))
                        Label(w.frame_tp2,text=str(clientlist[i][1]),font="Verdana 10").grid(row=int(sno), column=2, pady=(5))
                        Label(w.frame_tp2,text=str(ref.percentage),font="Verdana 10").grid(row=int(sno), column=3, pady=(5))
                        ##Label(w.frame_tp2,text=sno+".\t"+str(clientlist[i][0])+"\t"+str(clientlist[i][1])+"\tSending file ==>"+str(ref.percentage)).grid()
        w.frame_tp2.pack_propagate(0)
        w.frame_tp.pack()
        w.frame_tp2.pack()
        time.sleep(5)


def roundrobin():
    global thread_list1
    
    ##c=thread_list1.count()
    while True:
        for y in range(0,len(thread_list1)):
            if thread_list1[y]['sending']==1 and thread_list1[y]['pause']==0:
                ##print "Currntly active thread",x
                
                
                with all_false_lock:
                    thread_list1[y]['getlock']=True
                    print "=====thread set true=====",thread_list1[y]['thread']
                    print thread_list1

                while thread_list1[y]['getlock']:
                    pass
    
def startserver(w,path):
    threading.Thread(target=fun1 ,args=(w,path)).start()
    threading.Thread(target=roundrobin,args=()).start()
    threading.Thread(target=fun2 ,args=(w,)).start()
    


    
