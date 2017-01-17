from socket import *
import time
import pymedia.muxer as muxer, pymedia.audio.acodec as acodec, pymedia.audio.sound as sound
import time
import ast
##from Tkinter import *

complete=0
def play_mp3(soc,w):
    global complete
    dm= muxer.Demuxer('mp3')
    snds= sound.getODevices()
    snd= resampler= dec= None
    card=0
    rate=1
    tt=-1
    buf=soc.recv(1)
    sample_rate=int(soc.recv(int(buf)))
    channels=int(soc.recv(int(1)))
    print sample_rate,channels

    if snd== None:
        print 'Opening sound with %d channels -> %s' % ( channels, snds[ card ][ 'name' ] )
        snd= sound.Output( int( sample_rate* rate ), channels, sound.AFMT_S16_LE, card )

    while not complete:
        if w.play==1:
            while w.pause==0:
                print "in loop"
                buf=soc.recv(1)
                if buf=='s':
                    complete=1
                    print 'got end===loop break'
                    break
                print "buf :",buf
                buf2=soc.recv(int(buf))
                print "buf 2, frme size recived :",buf2
                data=''
                while len(data)!=int(buf2):
                    b=int(buf2)-len(data)
                    print "buffer length",b
                    data+=soc.recv(b)
                    print "data length",len(data)
                snd.play( data )
    ##soc.close()
    if w.stop!=1:
        w.change_button()
    complete=0
    w.play=1
    w.pause=0
    w.stop=0
    


    





