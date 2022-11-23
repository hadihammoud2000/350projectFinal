import socket
import sys
import os
import time

HOST = '0.0.0.0'                 
PORT = 38202
while(1):
    socketTemp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socketTemp.bind((HOST, PORT))
        #we use this socket temp in order to just comunicate the type of file transfer we want to use


    protocol,addr = socketTemp.recvfrom(1024)
    protocol=protocol.decode()
    print(protocol)
        #we initiate the connection and bind port and socket together
    #server tcp protocol by layan
   
    if protocol=="TCP":
        socketTemp.close()
                #if the user choses a tcp file transfer we close the temporary socket and 
        # create a new socket and bind port and host to make it fctnal 
       
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket1.bind((HOST, PORT))
                #we bind in this socket to use it
        
        def listToString(s): 
            str1 = ", "
            return (str1.join(s))
        socket1.listen(1)
                #since we are dealing with a tcp implementation , it is a characteristic of the protocol
        #to have the server always listening in on the socket and establishing a connection 
       
        while (1):
            conn, addr = socket1.accept()
            instruction = conn.recv(100).decode()
                        #we accept the connection done through the socket and recieve the instruction we want to implement
            #and decode it after having it sent encoded in bites by the client
            
            print ('Client> %s' %(instruction))
            if (instruction == 'quit'):
                conn.close()
                break
                        #the quit instruction will terminate the connection
           
            if (instruction == 'lsd'):
                sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                files = listToString(os.listdir())
                sockUDP.sendto(files.encode(),(addr[0], PORT))
                sockUDP.close()
                                #if we have a list instruction
                #the code will access the server directory and transform the list that contains
                #the names to a string that will be encoded and sent
               
            else:
    
                if (instruction == 'put'):
                                        #if we have a put instruction the client will upload a file to the server
                    #the code will create a file with the same name as the one being uploaded
                    #thanks to reqFile and it has the time to do so because of the sleep command 
                    #in the client that servers as a timeout to strat writting data inside the file
                   
                    bitrate=0.0
                    RecSoFar=0.0
                    req = conn.recv(100).decode()
                    
                    print(req)
                    #size = req[0]
                    reqFile = req
                    print ('Client> %s' %(reqFile))
                    
                    time.sleep(0.5)
                   # size = int(size)
                    with open(reqFile, 'wb') as reqFile:
                        T1 = time.time()
                                                    #we opened the file and we start recieving data through the socket
                            #and writting the data in the file in the server directory,
                            
                        while True:
                            data = conn.recv(102400)
                            RecSoFar += len(data)
                            timeSoFar = time.time()-T1
                            if timeSoFar !=0:
                
                               bitrate = RecSoFar/timeSoFar
                            print("real time bitrate: ",bitrate)
                            if not data:
                                          #once there is no more data to write the condition will fail and we exit the is statement
                            
                                break
                            reqFile.write(data)
                        reqFile.close()
        
                        
                    print ('Receive Successful')
                    
                elif (instruction == 'get'):
                    reqFile = conn.recv(100).decode()
                    print ('Client> %s' %(reqFile))
                    size = os.stat(reqFile)
                    sizeS = size.st_size
                    print(sizeS)
                    T1 = time.time()
                    with open(reqFile, 'rb') as reqFile:   
                        for data in reqFile:
                            conn.sendall(data)
                                                        #when thne client wants to download a file from the server
                            #the server receives the file name that is required , opens it i its directory
                            #and sends all the data trough the socket to the client
                  
                    print ('Send Successful')
                    totalTime = time.time()-T1
                    print(totalTime)
                    bandwidth = (sizeS*8)/totalTime
                    print("bandwidth: ",bandwidth)
            conn.close()      
        socket1.close()
                #when we are done we close all the sockets
    #server udp protocol by hadi
   

    elif protocol=="UDP":
        socketTemp.close()
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket1.bind((HOST, PORT))
                #we use this socket temp in order to just comunicate the type of file transfer we want to use

        def listToString(s): 
            str1 = ", " 
            return (str1.join(s))
        socket1.listen(1)
        while(1):
            conn, addr = socket1.accept()
            instruction = conn.recv(100).decode()
            print(instruction)
            instruction = instruction.split("##")
            reqFile = instruction[1]
            instruction = instruction[0]
            print ('Client> %s' %(instruction))
            if (instruction == 'quit'):
                conn.close()
                break
            elif(instruction=='lsd'):
                sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                files = listToString(os.listdir())
                sockUDP.sendto(files.encode(),(HOST, PORT))
                sockUDP.close()
                #same as tcp
            else:
                print ('Client> %s' %(reqFile))
                if (instruction == 'put'):
                    bitrate=0.0
                    RecSoFar=0.0
                    size = conn.recv(100).decode()
                    print(size)
                    print(reqFile)
                    sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sockUDP.bind((HOST,PORT)) #change to zeros
                    c = 0
                    init = 0

                    with open("UDP_"+reqFile, 'wb') as reqFile:
                      T1 = time.time()
                      while init<int(size):
                          data,addr = sockUDP.recvfrom(4096)
                          print(data)
                          reqFile.write(data)
                          RecSoFar += len(data)
                          timeSoFar = time.time()-T1
                          if timeSoFar !=0:
                
                               bitrate = RecSoFar/timeSoFar
                               print("real time bitrate: ",bitrate)
                          if not data:
                              break
                          init += len(data)
                          c+=1
                          print('packet number: ',c)
                          
                    reqFile.close()
                    sockUDP.close()
                          


                    
                    print ('Receive Successful')
                elif (instruction == 'get'):
                    size = os.stat(reqFile)
                    sizeS = size.st_size
                    conn.send((str(sizeS).encode()))
                    print(reqFile)
                    print(sizeS)
                    sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sockUDP.bind((HOST,PORT)) #change to zeros
                    ping, address = sockUDP.recvfrom(100)
                    c = 0

                    init = 0
                    print(sizeS)

                    with open(reqFile, 'rb') as readFile:
                            time.sleep(0.5)
                            T1 = time.time()
                            while init < int(sizeS):
                                data = readFile.read(4096)
                              
                                if not data:
                                    break
                                sockUDP.sendto(data,address)
                                init +=len(data)
                                c+=1
                                print("packet number: ",c)
                    totalTime = time.time()-T1
                    print(totalTime)
                    bandwidth = (sizeS*8)/totalTime
                    print("bandwidth: ",bandwidth)
                                

                    print ('Send Successful')
            conn.close() 
        socket1.close()