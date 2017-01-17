from socket import *
import os



def show_doc(s,f_name):
    f = open("files\\"+f_name,'wb')
    print "Receiving..."
    l=""
    len1=s.recv(1)
    len2=s.recv(int(len1))
    buf=int(len2)
    while len(l)<int(len2):
        print "Receiving..."
        l = l+s.recv(buf)
        buf=int(len2)-len(l)

    f.write(l)
    print 'recived fully'
    f.close()
    s.send("got file")
    path="files\\"+f_name
    os.startfile(path)
    return
