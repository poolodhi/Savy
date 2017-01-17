import sys,os
import subprocess

def rightpath(foldername,filename):
    ##cmd1="cd "+foldername
    if(foldername!=""):
        folder="\""+foldername+"\""
    else:
        folder=foldername
    cmd="ls "+folder
    try:
        ##subprocess.check_output(cmd1,shell=True)
        o=subprocess.check_output(cmd,shell=True)
        ##print o
        a=o.split("\n")
        ##print a
        f=open(filename+'.txt','w')
        for x in a:
            if(x.endswith(".mp3") or x.endswith(".mp4") or x.endswith(".doc") or x.endswith(".docx") or x.endswith(".pdf")):
                f.write(x+"\n")
            elif( '.' in x):
                pass
            else:
                f.write(x+"\n")
        f.close()
        return 1
    except:
        return 0
    
    

##print rightpath('C:\Users\MR. V.P. SINGH\Downloads','a.txt')


