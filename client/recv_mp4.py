from socket import *
import time
import subprocess
import os




def vedio_recv(soc):
    file_list=[]
    connerror=False
            
    j=0
    while True:
        f_name="files\Out"+str(j)+".mp4"
        f=open(f_name,'wb')
        
        file_list.append(f_name)
        b=soc.recv(1)
        if int(b)==0:
            soc.send("stop")
            print "=========DATA COMPLETED==========="
            
            for x in file_list:
                os.remove(x)
            file_list=[]
            ##print soc.recv(1)
            break
        buf=soc.recv(int(b))
        print buf
        length=int(buf)
        print buf
        total=0
        while True:
            if(length-total<1024 and total!=length):
                print "inside lesse"
                data=soc.recv(length-total)
                f.write(data)
                total+=len(data)
                print "=================got one file===================="
                break
                
            else:
                data=soc.recv(1024)
                f.write(data)
            total+=len(data)
        f.close()
        if (j==5):
            play_vedio(file_list)
        if j>5:
            if add_to_list(j,file_list):
                pass
            else:
                soc.send("stop")
                print "=========connection error stoped getting data==========="
                print file_list
                
                ##for x in file_list:
                ##    os.remove(x)
                file_list=[]
                print file_list
                print soc.recv(1)
                break
            ##add_to_list(j)
        j=j+1


def play_vedio(file_list):
    j=0
    while j<=5:
        filename="out"+str(j)+".mp4"
        a=subprocess.Popen(["C:\Program Files (x86)\VideoLAN\VLC\\vlc.exe","--started-from-file","--playlist-enqueue","--play-and-exit","--no-video-title",file_list[j]])
        ##a.wait()
        time.sleep(1)
        j+=1
        
def add_to_list(index,file_list):
    cmd="tasklist |grep vlc.exe"
    try:
        o=subprocess.check_output(cmd,shell=True)
        ##print o
        a=subprocess.Popen(["C:\Program Files (x86)\VideoLAN\VLC\\vlc.exe","--started-from-file","--playlist-enqueue","--play-and-exit","--no-video-title",file_list[index]])
        return True
    except:
        return False
