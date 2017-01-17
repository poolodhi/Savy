from socket import *
import os

def show_pdf(s,f_name):
    f = open("files\\"+f_name,'wb')
    print "Receiving..."
    l=""
    while True:
        print "Receiving..."
        l = s.recv(1024)
        ##print l
        f.write(l)
        if l.endswith("EOF\n") or l.endswith("EOF"):
            break
    print 'recived fully'
    f.close()
    s.send("got file")
    path="files\\"+f_name
    os.startfile(path)
    return
    
