import socket
import sys
import os
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from os import path
#we import all the libraries needed

main = Tk()
main['bg']="white"
main.title("UTransfer")
main.geometry('800x500')
#by karl
#we abstract the code and the console with the help of a tkinter-based GUI that appears 
#as soon as we run the client
#we open a window 'main' to choose between a UDP or TCP protocol 


def TCPfunc():
        #as soon as we chose TCP protocol or UDP the mian window will close and 
    #an auxiliary TCPtransfer/UDPtranfer window will pop up
    #depending on what we chose
    main.destroy()
    tcp_window = Tk()
    tcp_window['bg']="white"
    tcp_window.title("UTransfer TCP")
    tcp_window.geometry("800x500")
    lab1 = Label(tcp_window, text='Welcome to UTransfer TCP!', font=('times new roman',30), bg="white",fg="green")
    lab1.grid(column=1, row=0)
    socketTemp.sendto(b'TCP',(HOST,PORT))
        #send the protocol to the server in bites

    socketTemp.close()
    #function : TCPfunct() by karl

    def put_TCP(inputFile):
        #put_TCP fct by layan
        size = os.stat(inputFile)
        sizeS = size.st_size
        #we use the size and OS library in order to make our avr bandwith calculating in bites per sec
        
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket1.connect((HOST, PORT))
        #initiate a socket and connect the host and port
        
        instruction = 'put'
        socket1.send(instruction.encode())
        time.sleep(0.5)
        socket1.send(inputFile.encode())
         #we send the instruction to the server encoded in binary
       
         #the sleep command is used to account for the lack of syncing between the client and
        #server and client , this way the server will have time to create the file and recieve the data to 
        #put in it rather than have the data recieved too fast and be put in the file name
        # #rather than the file itself 
       
        with open(inputFile, 'rb') as file_to_send:
            T1=time.time()
            for data in file_to_send:
                socket1.sendall(data)
        totalTime=time.time()-T1
                    #we open the file we want to transfer and we find it by name, then we send all the data
                #in the file to the server through the socket that we opened
                #we find the total time it took to send the data
        #and we account for the error we get if the time is too small to be quantified and calculated by python
        #we give total time an insignificant value just to not get a division by 0
        #we calculating the bandwidth
       
        if totalTime == 0:
            totalTime = 0.000001    
        bandwidth=(sizeS*8)/totalTime
        lab=Label(tcp_window,text=str((bandwidth)*(10**(-6))))
                #bitrate and bandwith calculations of sender/upload by karl
        #we display the avr bandwidth in the tkinter window
       
        lab.grid(column=0,row=6)
        messagebox.showinfo("UResult","Upload Successful!")
        socket1.close()
        #message box by karl and label
        return
    def put_func():
                #put_func()by karl and mariam
        #we use this function in order to access the OS and open a window of a specified directory
        #we note that this function does not return the file name which is what we need
        #it returns the directory so we simply split it by the / and take the last element which 
        #will be the file name needed to make the transfer work
       
        file = filedialog.askopenfilename(initialdir=path.dirname(__file__))
        filename=file.split('/')
        print(filename[-1])
        put_TCP(filename[-1])
             #we call the put_TCP fct with the retreived filename in order to upload said file to server
    
        return
    def get_TCP(inputFile):
           #get_TCP function by layan
        #function to download from the server
        
        bitrate=0.0
        RecSoFar=0.0
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket1.connect((HOST, PORT))
            #initiate a socket and connect the host and port
        
        instruction = 'get'
        socket1.send(instruction.encode())
        #inputFile = input("enter file name: ")
        time.sleep(0.5)
          #same reason to use it as before 
        
        socket1.send(inputFile.encode())
        with open(inputFile, 'wb') as file_to_write:
            T1 = time.time()
                        #we sample the time before starting to receive and we save it as T1
            #and we have a recsofar var in order to calculate a dynamic bitrate while downloading
            #this bitrate will be calculated with each iteration and implementation of the sockect.rec command
                        
           
            while True:
                data = socket1.recv(102400)
                RecSoFar += len(data)
                timeSoFar = time.time()-T1
                if timeSoFar !=0:
                    bitrate = RecSoFar/timeSoFar
                    print("real time bitrate: ",bitrate)
               #reciever bitrate by mariam
                if not data:
                    break    
                file_to_write.write(data)
        file_to_write.close()
        #when we are done downloading we close the file to write
        lab=Label(tcp_window,text=str(bitrate*(10**(-6))))
        lab.grid(column=0,row=7)
        messagebox.showinfo("UResult","Download Successful!")
        #lab=Label(tcp_window, text="Download Successful!", font=('times new roman',15), bg="white",fg="green")
        #lab.grid(column=4, row=3)
        socket1.close()
        return
    def get_func():
        #get_func() by karl
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket1.connect((HOST, PORT))
         #we connect host and port with the socket
        
        instruction = 'lsd'
                #we use this instruction to list all the files in the server
        #note that we cannot use the method implemented for the upload 
        #because when it comes to uploading we are simply opening a directory 
        #in our PC whereas in this case we download from the server which is not on
        #our client device so we simply send the file name list from the server
        #and display them in the client interface
       
        socket1.send(instruction.encode())
           #we send the instruction to the server so it knows what instruction the client chose

        socket1.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0',PORT))
                #create a new socket for which we recieve the list of items in the directory of the server
        #after recieveing it we decode it and split by comas to display later , each file seperately 

       
        files =(sock.recv(100).decode()).split(",")
        sock.close()
        dir_window = Tk()
        dir_window['bg']="white"
        dir_window.title("Download List")
        dir_window.geometry('300x300')
                #window by mariam
        #we create a new tkinter window just to print the downloadable files from the server
        #note that we use a new window because labels cannot be updated , when they are displayed they are constant so when we reupload
        #a file to tyhe server we will get a new updated window from scratch rather than having overlapping labels in our main window

        for i in range (len(files)):
            lab = Label(dir_window,text=str(files[i]),font=('times new roman',10), bg="white",fg="green")
            lab.grid(column=0,row=i)
                  #we display a label with a file name for each iteration while looping
       
        fileName = Entry(tcp_window, width=20)
        fileName.grid(column=2,row=3)
          #entry text box to type the name of the file that we wish to download 
        
        ent = Button(tcp_window, text="ENTER",bg="white", fg="green", command=lambda:get_TCP(fileName.get()))
        ent.grid(column=3,row=3)
        #the button is used to initiate the download:when pressed, it retreaves the name and uses it as parameter to get_TCP fct

        dir_window.mainloop()
        
        #download list gui implementation by karl
       
        return

    lb=Label(tcp_window,text='',bg="white")
    lb.grid(column=1,row=1)
      #buffer labels just to space out the design
   

    putbutton = Button(tcp_window, text="Upload", bg="white", font=('times new roman',10), fg="black",command=lambda:put_func(), padx=15, pady=10)
    putbutton.grid(column=1,row=2)
        #put button to initiate the put fct
    #file = filedialog.askopenfilename(initialdir=path.dirname(__file__))


    getbutton = Button(tcp_window, text="Download", bg="white", font=('times new roman',10), fg="black",command=lambda:get_func(), padx=15, pady=10)
    getbutton.grid(column=1,row=3)
    #get button to download from the server
    tcp_window.mainloop()
      #putbuton and getbutton implementation by mariam


def UDPfunc():
       #UDPfunc()by mariam
    #initiate a UDP window and distroy the main one
   
    main.destroy()
    udp_window = Tk()
    udp_window['bg']="white"
    udp_window.title("UTransfer UDP")
    udp_window.geometry("800x500")
    lab1 = Label(udp_window, text='Welcome to UTransfer UDP!', font=('times new roman',30), bg="white",fg="green")
    lab1.grid(column=1, row=0)
    socketTemp.sendto(b'UDP',(HOST,PORT))
      #comunicate the transfer type from the client to the server
    
    socketTemp.close()

    def put_UDP(inputFile):
                #put_UDP by hadi
        #get the size of file to upload
       
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket1.connect((HOST, PORT))
        instruction = 'put'
        temp = instruction + "##" + inputFile
        socket1.send(temp.encode())
        size = os.stat(inputFile)
        sizeS = size.st_size
        time.sleep(0.5)

        socket1.send(str(sizeS).encode())
        socket1.close()

        socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        c = 0

        init = 0
        print(sizeS)

        with open(inputFile, 'rb') as readFile:
             time.sleep(0.5)
             T1 = time.time()
             while init < int(sizeS):
                data = readFile.read(4096)
        
                if not data:
                    break
                socket2.sendto(data,(HOST,PORT))
                init +=len(data)
                c+=1
                print("packet number: ",c)
        totalTime=time.time()-T1
        bandwidth=(sizeS*8)/totalTime
        lab=Label(udp_window,text=str((bandwidth)*(10**(-6))))
        lab.grid(column=0,row=6)
                
           #upload /sender bitrate by karl


        


        

        #send file
        socket2.close()
        print("put UDP")
        print(inputFile)
        messagebox.showinfo("UResult","Upload Successful!")
        return
    def put_func():
        #put_func()#by karl and mariam
        print("in put func")
        file = filedialog.askopenfilename(initialdir=path.dirname(__file__))
        filename=file.split('/')
        print(filename[-1])
        put_UDP(filename[-1])
        return
    def get_UDP(inputFile):
        #get_UDP fct by hadi
        bitrate=0.0
        RecSoFar=0.0
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket1.connect((HOST, PORT))
        instruction = 'get'
        temp = instruction + "##" + inputFile
        socket1.send(temp.encode())
        size=socket1.recv(100).decode()
        size = int(size)
        print(size)
        socket1.close()
        socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket2.sendto(b'ping',(HOST,PORT))
        c = 0
        init = 0

        with open("UDP_"+inputFile, 'wb') as reqFile:
            T1 = time.time()
            while init<int(size):
                data,addr = socket2.recvfrom(4096)
                print(data)
                reqFile.write(data)
                RecSoFar += len(data)
                timeSoFar = time.time()-T1
                if timeSoFar !=0:
                    bitrate = RecSoFar/timeSoFar
                    
                    #receiver bitrate by mariam
                    print("real time bitrate: ",bitrate)
                if not data:
                    break
                init += len(data)
                c+=1
                print('packet number: ',c)


        socket2.close()
        lab=Label(udp_window,text=str(bitrate*(10**(-6))))
        messagebox.showinfo("UResult","Download Successful!")
        print("get UDP")
           #display a window that gives thnis message each time the transfer is succesfull rather than having
        #a fixed label that will stay here constantly
        
        print(inputFile)
        return
    def get_func():
        #get_func() by mariam
        print("in get func")
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket1.connect((HOST, PORT))
        instruction = 'lsd'
        temp = instruction+"##"+"\\\\"
        socket1.send(temp.encode())
        socket1.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0',PORT))
        files =(sock.recv(100).decode()).split(",")
        sock.close()
        dir_window = Tk()
        dir_window['bg']="white"
        dir_window.title("Download List")
        dir_window.geometry('300x300')
        for i in range (len(files)):
            lab = Label(dir_window,text=str(files[i]),font=('times new roman',10), bg="white",fg="green")
            lab.grid(column=0,row=i)
        fileName = Entry(udp_window, width=20)
        fileName.grid(column=2,row=3)
        ent = Button(udp_window, text="ENTER",bg="white", fg="green", command=lambda:get_UDP(fileName.get()))
        ent.grid(column=3,row=3)
        dir_window.mainloop()
        #dir_window.destroy()
        return


    lb=Label(udp_window,text='',bg="white")
    lb.grid(column=1,row=1)

    putbutton = Button(udp_window, text="Upload", bg="white", font=('times new roman',10), fg="black",command=lambda:put_func(), padx=15, pady=10)
    putbutton.grid(column=1,row=2)

    getbutton = Button(udp_window, text="Download", bg="white", font=('times new roman',10), fg="black",command=lambda:get_func(), padx=15, pady=10)
    getbutton.grid(column=1,row=3)
    udp_window.mainloop()
    #lb , putbuton, getbutton by mariam


#this is the part where we implemented the main interface using tkinter

lab1 = Label(main, text='Welcome to UTransfer!', font=('times new roman',30), bg="white",fg="green")
lab1.grid(column=1, row=0)

lab1 = Label(main, text='', bg="white")
lab1.grid(column=0,row=1)

lab2 = Label(main, text='Click here for TCP Transfer:', fg="green", bg="white", font=('times new roman',15))
lab2.grid(column=0, row=2)

TCPbutton = Button(main, text="TCP", bg="white", font=('times new roman',10), fg="black",command=lambda:TCPfunc(), padx=15, pady=10)
TCPbutton.grid(column=1, row=2)
#to redirect us to the tcp protocol fcts in a new window


lab3 = Label(main, text='',bg="white")
lab3.grid(column=1,row=3)

lab4 = Label(main, text='Click here for UDP Trasnfer:', fg="green", bg="white", font=('times new roman',15))
lab4.grid(column=0, row=4)

UDPbutton = Button(main, text="UDP",bg="white", fg="black",font=('times new roman',10),command=lambda:UDPfunc(), padx=15, pady=10)
UDPbutton.grid(column=1, row=4)
#lab1,2,3,4.udpbuton,tcpbutton by karl
#to redirect us to the udp protocol window 


HOST = '192.168.0.116'   
PORT = 38202




#create UDP socket to agree on protocol
socketTemp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#protocol = input("Enter TCP or UDP: ")

main.mainloop()