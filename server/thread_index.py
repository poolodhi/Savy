import threading
thread_list1=[]##for roound robin
thread_list2=[]
all_false_lock = threading.Semaphore(1) 


all_false=1

##{'thread':t,'getlock':False,'ipaddr':addr[0],'port':addr[1],'conn_obj':conn}

def getindex_connobj_1(i):
    
    for a in range(0,len(thread_list1)):
        if thread_list1[a]['ipaddr']==i[0] and thread_list1[a]['port']==i[1]:
            print "returning thread ",thread_list1[a]['thread']
            return a

    return -1


        
    
