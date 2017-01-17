
import pymedia.muxer as muxer, pymedia.audio.acodec as acodec, pymedia.audio.sound as sound
import time
import sys
import thread


def fun_recv(comm_obj):
    while True:
        if comm_obj.complete==1:
            print 'in complete:',comm_obj.Pause,"complete:",comm_obj.complete,"play:",comm_obj.Play
            break
        
        a=comm_obj.c.recv(4)
        if comm_obj.type=='m':
            a=a.rstrip("\n")
            
        if(a=='stop' or a=='sto'):
            print '=================got stop====================='
            ##if comm_obj.type=='m':
                ##print 's send from stop'
                ##comm_obj.c.send('s')
            comm_obj.complete=1
            comm_obj.Stop=1
            comm_obj.Play=0
            comm_obj.Pause=0
            print 'in stop:',comm_obj.Pause,"complete:",comm_obj.complete,"play:",comm_obj.Play
            break
##        elif(a=='paus'):
##            print "==============got pause===================="
##        elif(a=='play'):
##            print "==============got play===================="
        elif(a=='endd' or 'end'):
            break
        else:
            print 'in pause:',comm_obj.Pause,"complete:",comm_obj.complete,"play:",comm_obj.Play
            print '=================invalid option ============='


def start_send(comm_obj,filename):
    if comm_obj.type=='l' or comm_obj.type=='m' :
        thread.start_new_thread(fun_recv,(comm_obj,))
    dm= muxer.Demuxer('mp3')
    f= open(filename, 'rb' )
    f1= open(filename, 'rb' )
    filetotal=len(f1.read())
    snd= resampler= dec= None
    info=None
    s= f.read( 32000 )
    ##print len(s)  
    t= 0
    dec=None
    i=0
    total_send=0
    print 'sending mp3 file to :',comm_obj.addr
    while len( s ):
        
        total_send+=len(s)
        frames= dm.parse( s )
        if frames:
            pre=(total_send/float(filetotal))*100
            comm_obj.percentage=round(pre,2)
            print "precentage send=====>",str(comm_obj.percentage)
            for fr in frames:
                if dec== None:
                  print dm.streams[ fr[ 0 ] ]
                  dec= acodec.Decoder( dm.streams[ fr[ 0 ] ] )
                  print dec
                
                r= dec.decode( fr[ 1 ] )
                if(comm_obj.type=='l'):
                    if info==None:
                        comm_obj.c.send(str(len(str(r.sample_rate))))
                        comm_obj.c.send(str(r.sample_rate))
                        comm_obj.c.send(str(r.channels))
                        info='send'
                        
                if(comm_obj.type=='m'):
                    if info==None:
                        print "sending samplerate"
                        comm_obj.c.send(str(r.sample_rate)+"\n")
                        info='send'
                    
                if r and r.data:
                    i=1+i
                    if i>=0:
                        data_string=r.data
                        print len(data_string)
                        l=len(data_string)
                        l1=len(str(l))
                        if(comm_obj.type=='l'):
                            comm_obj.c.send(str(l1))
                            comm_obj.c.send(str(l))
                        print 'size len',l
                        print 'frame size',l1
                        comm_obj.c.send(data_string)
                        
##                        if comm_obj.Pause==1:
##                            print 'in pause:',comm_obj.Pause,"complete:",comm_obj.complete,"play:",comm_obj.Play
##                            Start_frame=i
##                            return
                        
                        if comm_obj.Stop==1:
                            return
              
        s= f.read( 512 )
    comm_obj.complete=1

def sendfile_mp3(comm_obj,filename):
    comm_obj.sending=1
    while not comm_obj.complete:
        ##print "complete:",comm_obj.complete
        if comm_obj.Play==1:
            start_send(comm_obj,filename)
    print 's send'
    comm_obj.c.send('s')
    ##print 's send'
    comm_obj.Pause=0
    comm_obj.Play=1
    comm_obj.Start_frame=0
    comm_obj.complete=0
    comm_obj.Stop=0
    comm_obj.percentage=0
    comm_obj.sending=0

    
