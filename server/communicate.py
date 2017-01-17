from socket import *
import os, sys

from folder_maker import *
from send_mp3_file import *
from send_mp4_file import *
from pdf_send import *
from doc_send import *


clientlist=[]
active_extrainfo=[]

class communicate:
    def __init__(self,conn,addr,path):
        print "----------new thread start-----"
        self.c=conn
        self.addr=addr
        self.path=path
        self.clientname="_c"+str(addr[1])
        self.Pause=0
        self.Play=1
        self.Start_frame=0
        self.complete=0
        self.Stop=0
        self.percentage=0
        self.sending=0
        self.type='m'

    def set_path(self,f):
        self.path=f
    def return_path(self):
        return self.path
    def return_addr(self):
        return self.addr
    def retrun_clientname(self):
        return self.clientname
    def set_type(self,type1):
        self.type=type1
    
    def send_folder_list(self,filename):
        print "In sendfolder function"
        f=open(filename)
        for line in iter(f):
            ##print "folder name",line
            if(self.type=='m'):
                if(line!="\n"):
                    self.c.send(line)
            if(self.type=='l'):
                self.c.send(line)
                print self.c.recv(1)
        self.c.send('end\n')
        if(self.type=='l'):
            print self.c.recv(1)

    def send_mp3(self,mp3file):
        f=self.return_path()+"\\"+mp3file
        self.string_print="Streaming :\t"+mp3file
        print f
        sendfile_mp3(self,f)
        
    def send_mp4(self,mp4file):
        f=self.return_path()+"\\"+mp4file
        self.string_print="Streaming :\t"+mp4file
        print f
        sendfile_mp4(f,self)
    
    def send_pdf(self,pdffile):
        f=self.return_path()+"\\"+pdffile
        self.string_print="Sending :\t"+pdffile
        print f
        send_pdf_file(self,f)

    def send_doc(self,docfile):
        f=self.return_path()+"\\"+docfile
        self.string_print="Sending :\t"+docfile
        print f
        send_doc_file(self,f)

    def recv_data(self):
        self.data=self.c.recv(1024)
        print "Recived request"+str(self.addr[1])+"===>data:"+self.data
        return self.data

    def close(self):
##        self.conn.close()
        clientlist.remove(self.addr)
        self.c.close()
        print "--------------connection closed----------"
