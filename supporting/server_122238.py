import socket
import sys
import os
import time

HOST = '0.0.0.0'
PORT = 32020
while(1):
    socketTemp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socketTemp.bind((HOST, PORT))

    protocol,addr = socketTemp.recvfrom(1024)
    protocol=protocol.decode()
    print(protocol)
    if protocol=="TCP":
        socketTemp.close()
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket1.bind((HOST, PORT))
        def listToString(s):
            str1 = ", "
            return (str1.join(s))
        socket1.listen(1)
        while (1):
            conn, addr = socket1.accept()
            instruction = conn.recv(100).decode()
            print ('Client> %s' %(instruction))
            if (instruction == 'quit'):
                conn.close()
                break
            if (instruction == 'lsd'):
                sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                files = listToString(os.listdir())
                sockUDP.sendto(files.encode(),(addr[0], PORT))
                sockUDP.close()
            else:

                if (instruction == 'put'):
                    bitrate=0.0
                    RecSoFar=0.0
                    req = conn.recv(100).decode()

                    print(req)
                    #size = req[0]
                    reqFile = req
                    print ('Client> %s' %(reqFile))

                    time.sleep(0.5)
                   # size = int(size)
                    with open("TCP_"+reqFile, 'wb') as reqFile:
                        T1 = time.time()
                        while True:
                            data = conn.recv(102400)
                            print(data)
                            RecSoFar += len(data)
                            timeSoFar = time.time()-T1
                            if timeSoFar !=0:

                               bitrate = RecSoFar/timeSoFar
                            print("real time bitrate: ",bitrate)
                            if not data:
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
                    print ('Send Successful')
                    totalTime = time.time()-T1
                    print(totalTime)
                    bandwidth = (sizeS*8)/totalTime
                    print("bandwidth: ",bandwidth)
            conn.close()
        socket1.close()

    elif protocol=="UDP":
        socketTemp.close()
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket1.bind((HOST, PORT))
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
                sockUDP.sendto(files.encode(),(addr[0], PORT))
                sockUDP.close()
            else:
                print ('Client> %s' %(reqFile))
                if (instruction == 'put'):
                    bitrate=0.0
                    RecSoFar=0.0
                    size = conn.recv(100).decode()
                    print(size)
                    print(reqFile)
                    sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sockUDP.bind(('0.0.0.0',PORT)) #change to zeros
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
                    sockUDP.bind(('0.0.0.0',PORT)) #change to zeros
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
