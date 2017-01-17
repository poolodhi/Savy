from moviepy.editor import *
import sys,os
import subprocess
from socket import *
from thread_index import *
import time
import thread

def fun_recv(comm_obj):
    global thread_list1
    thread_index=getindex_connobj_1(comm_obj.addr)
    while True:
        
        a=comm_obj.c.recv(4)
        if comm_obj.type=='m':
            a=a.rstrip("\n")
        if(a=='stop' or a=='sto'):
            ##if comm_obj.type=='m':
                ##comm_obj.c.send('3')
                ##comm_obj.c.send("end")
            print '=================got stop====================='
            comm_obj.complete=1
            with all_false_lock:
                thread_list1[thread_index]['getlock']=False
                thread_list1[thread_index]['sending']=False
            ##comm_obj.Stop=1
            ##comm_obj.Play=0
            ##comm_obj.Pause=0
            print 'in stop:',comm_obj.Pause,"complete:",comm_obj.complete,"play:",comm_obj.Play
            break
        elif(a=='endd' or 'end'):
            break
        else:
            print 'in pause:',comm_obj.Pause,"complete:",comm_obj.complete,"play:",comm_obj.Play
            print '=================invalid option ============='


def send_vedio(filename,comm_obj):
    global thread_list1
    
    thread_index=getindex_connobj_1(comm_obj.addr)
    tot=0;
    last=0;
    f=open(filename,'rb')
    f1=open(filename,'rb')
    length=len(f1.read())
    print "length"+str(length)
    f1.close()
    if comm_obj.type=='l':
        if comm_obj.complete!=1:
            comm_obj.c.send(str(len(str(length))))
            comm_obj.c.send(str(length))
            ##time.sleep(1)
        else:
            return
    
    ##comm_obj.send(str(length)+'\n')
    if comm_obj.type=='m':
        if comm_obj.complete!=1:
            comm_obj.c.send(str(len(str(length))))
            comm_obj.c.send(str(length))
            time.sleep(1)
        else:
            return
    l = f.read(1024)
    tot+=1024
    while l:
        start_time=time.time()
        if thread_list1[thread_index]['getlock']:
            while (l):
                last=length-tot
                print "sending to ",thread_list1[thread_index]['thread'],"at port",comm_obj.addr[1]
                comm_obj.c.send(l)
                if last<1024 and last>0 :
                    print "last packet sending........................",last
                    l=f.read(last)
                    tot+=last
                    ##print tot
                else:
                    l = f.read(1024)
                    tot+=1024

                timer=time.time()-start_time
                if(timer>10):
                    print "timer over at:::",timer
                    with all_false_lock:
                        thread_list1[thread_index]['getlock']=False
                    timer=0
                    break
                if comm_obj.complete==1:
                    with all_false_lock:
                        thread_list1[thread_index]['getlock']=False
                        l=""
                    break

                #print l
    f.close()
    with all_false_lock:
        thread_list1[thread_index]['getlock']=False
    print "=======file send completely======"
        



##filename="l.mp4"

def crop_file(filename,comm_obj):
    global thread_list1

    thread_index=getindex_connobj_1(comm_obj.addr)
    with all_false_lock:
        thread_list1[thread_index]['sending']=True

    if comm_obj.type=='l' or comm_obj.type=='m':
        thread.start_new_thread(fun_recv,(comm_obj,))
        
    cmd="ffprobe -i \""+filename+"\" -show_format | grep duration"
    o=subprocess.check_output(cmd,shell=True)
    print o
    dot_index=o.find('.')
    print dot_index
    if(dot_index>0):
        o=o[9:dot_index]
    else:
        o=o[9:]
    print o
    time1=int(o)
    print time1
    i=0

    if time1<300:
        x=5
    elif time1<500:
        x=10
    else:
        x=30
        
    end_t=0
    j=0
    flag=True
    while end_t<time1:
        
        
        
        print "end time ",end_t
        if comm_obj.type=='l':
            if comm_obj.complete==1:
                print "comm_obj.complete==1"
                comm_obj.c.send('0')
                flag=False
                with all_false_lock:
                    thread_list1[thread_index]['sending']=False
                break
        if comm_obj.type=='m':
            if comm_obj.complete==1:
                 print "comm_obj.complete==1 by m"
                 comm_obj.c.send('3')
                 comm_obj.c.send("end")
                 flag=False
                 with all_false_lock:
                     thread_list1[thread_index]['sending']=False
                 break
        clip = VideoFileClip(filename).subclip(i,i+x)
        clip.write_videofile("out"+comm_obj.clientname+".mp4",fps=24, codec='mpeg4')
        send_vedio("out"+comm_obj.clientname+".mp4",comm_obj)
        i+=x
        end_t=end_t+x
        pre=(end_t/float(time1))*100
        print "preceitage",pre
        comm_obj.percentage=round(pre,2)
        if (time1-end_t<x):
            x=time1-end_t
            ##print x
        ##if j>10:
            ##comm_obj.c.send('0')
            ##break
                ##if j==5:
            ##time.sleep(60)
        
        j+=1

    print end_t
    print "over"
    if comm_obj.type=='m':
        if flag:
            comm_obj.c.send('3')
            comm_obj.c.send("end")
    if comm_obj.type=='l':
        if flag:
            comm_obj.c.send('0')
    with all_false_lock:
                thread_list1[thread_index]['sending']=False
    os.remove("out"+comm_obj.clientname+".mp4")

def sendfile_mp4(filename,comm_obj):
    comm_obj.sending=1
    crop_file(filename,comm_obj)
    comm_obj.Pause=0
    comm_obj.Play=1
    comm_obj.Start_frame=0
    comm_obj.complete=0
    comm_obj.Stop=0
    comm_obj.percentage=0
    comm_obj.sending=0
    
