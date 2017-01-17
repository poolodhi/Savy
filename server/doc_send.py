from socket import *
from thread_index import *
import time

def send_doc_file(comm_obj,filename):
    global thread_list1
    thread_index=getindex_connobj_1(comm_obj.addr)
    with all_false_lock:
        thread_list1[thread_index]['sending']=True
        
    comm_obj.sending=1
    f=open(filename,'rb')
    f1=open(filename,'rb')
    file_len=len(f1.read())
    lendata=0

    if(comm_obj.type=='m'):
        comm_obj.c.send(str(file_len)+"\n")
    
    if(comm_obj.type=='l'):
        
        s1=len(str(file_len))
        comm_obj.c.send(str(s1))
        comm_obj.c.send(str(file_len))
    
    
    l = f.read(1024)
    while (l):
        start_time=time.time()
        if thread_list1[thread_index]['getlock']:
            while (l):
                lendata+=len(l)
                pre=(lendata/float(file_len))*100
                comm_obj.percentage=round(pre,2)
                print "send data ",lendata,thread_list1[thread_index]['thread'],"at port",comm_obj.addr[1]

                comm_obj.c.send(l)
                l = f.read(1024)
                timer=time.time()-start_time
                if(timer>5):
                    print "timer over at::::",timer
                    with all_false_lock:
                        thread_list1[thread_index]['getlock']=False
                    timer=0
                    break
                if pre==100:
                    with all_false_lock:
                        thread_list1[thread_index]['getlock']=False
                        thread_list1[thread_index]['sending']=False
    with all_false_lock:
        thread_list1[thread_index]['sending']=False
                    
    f.close()
    
    if(comm_obj.type=='l'):
        print comm_obj.c.recv(8)
        ##comm_obj.c.shutdown(SHUT_WR)
        ##comm_obj.c.send('yet there')
    print 'DOC file send completely'

    
    if(comm_obj.type=='m'):
        ##print "empty recvied",comm_obj.c.recv(2).rstrip("\n")
        ##comm_obj.c.send('s')
        print 'send... completed to mobile'

    comm_obj.percentage=0
    comm_obj.sending=0
