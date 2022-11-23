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

main = Tk()
main['bg']="white"
main.title("UTransfer")
main.geometry('800x500')

def TCPfunc():
    main.destroy()
    tcp_window = Tk()
    tcp_window['bg']="white"
    tcp_window.title("UTransfer TCP")
    tcp_window.geometry("800x500")
    lab1 = Label(tcp_window, text='Welcome to UTransfer TCP!', font=('times new roman',30), bg="white",fg="green")
    lab1.grid(column=1, row=0)
    socketTemp.sendto(b'TCP',(HOST,PORT))
    socketTemp.close()

    def put_TCP(inputFile):
        size = os.stat(inputFile)
        sizeS = size.st_size
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket1.connect((HOST, PORT))
        instruction = 'put'
        socket1.send(instruction.encode())
        time.sleep(0.5)
        socket1.send(inputFile.encode())
        time.sleep(0.5)
        with open(inputFile, 'rb') as file_to_send:
            T1=time.time()
            for data in file_to_send:
                socket1.sendall(data)
        totalTime=time.time()-T1
        if totalTime == 0:
            totalTime = 0.000001    
        bandwidth=(sizeS*8)/totalTime
        lab=Label(tcp_window,text=str((bandwidth)*(10**(-6))))
        lab.grid(column=0,row=6)
        messagebox.showinfo("UResult","Upload Successful!")
        socket1.close()
        return
    def put_func():
        file = filedialog.askopenfilename(initialdir=path.dirname(__file__))
        filename=file.split('/')
        print(filename[-1])
        put_TCP(filename[-1])
        return
    def get_TCP(inputFile):
        bitrate=0.0
        RecSoFar=0.0
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket1.connect((HOST, PORT))
        instruction = 'get'
        socket1.send(instruction.encode())
        #inputFile = input("enter file name: ")
        time.sleep(0.5)
        socket1.send(inputFile.encode())
        with open(inputFile, 'wb') as file_to_write:
            T1 = time.time()
            while True:
                data = socket1.recv(102400)
                RecSoFar += len(data)
                timeSoFar = time.time()-T1
                if timeSoFar !=0:
                    bitrate = RecSoFar/timeSoFar
                    print("real time bitrate: ",bitrate)
                if not data:
                    break    
                file_to_write.write(data)
        file_to_write.close()
        lab=Label(tcp_window,text=str(bitrate*(10**(-6))))
        lab.grid(column=0,row=7)
        messagebox.showinfo("UResult","Download Successful!")
        #lab=Label(tcp_window, text="Download Successful!", font=('times new roman',15), bg="white",fg="green")
        #lab.grid(column=4, row=3)
        socket1.close()
        return
    def get_func():
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket1.connect((HOST, PORT))
        instruction = 'lsd'
        socket1.send(instruction.encode())
        socket1.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0',PORT))
        files =(sock.recv(1000).decode()).split(",")
        sock.close()
        dir_window = Tk()
        dir_window['bg']="white"
        dir_window.title("Download List")
        dir_window.geometry('300x300')
        for i in range (len(files)):
            lab = Label(dir_window,text=str(files[i]),font=('times new roman',10), bg="white",fg="green")
            lab.grid(column=0,row=i)
        fileName = Entry(tcp_window, width=20)
        fileName.grid(column=2,row=3)
        ent = Button(tcp_window, text="ENTER",bg="white", fg="green", command=lambda:get_TCP(fileName.get()))
        ent.grid(column=3,row=3)
        dir_window.mainloop()
        #dir_window.destroy()
        return

    lb=Label(tcp_window,text='',bg="white")
    lb.grid(column=1,row=1)

    putbutton = Button(tcp_window, text="Upload", bg="white", font=('times new roman',10), fg="black",command=lambda:put_func(), padx=15, pady=10)
    putbutton.grid(column=1,row=2)
    #file = filedialog.askopenfilename(initialdir=path.dirname(__file__))

    getbutton = Button(tcp_window, text="Download", bg="white", font=('times new roman',10), fg="black",command=lambda:get_func(), padx=15, pady=10)
    getbutton.grid(column=1,row=3)
    tcp_window.mainloop()

def UDPfunc():
    main.destroy()
    udp_window = Tk()
    udp_window['bg']="white"
    udp_window.title("UTransfer UDP")
    udp_window.geometry("800x500")
    lab1 = Label(udp_window, text='Welcome to UTransfer UDP!', font=('times new roman',30), bg="white",fg="green")
    lab1.grid(column=1, row=0)
    socketTemp.sendto(b'UDP',(HOST,PORT))
    socketTemp.close()

    def put_UDP(inputFile):
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
        if totalTime==0:
            totalTime = 0.000001
        bandwidth=(sizeS*8)/totalTime
        lab=Label(udp_window,text=str((bandwidth)*(10**(-6))))
        lab.grid(column=0,row=6)
                
           


        


        

        #send file
        socket2.close()
        print("put UDP")
        print(inputFile)
        messagebox.showinfo("UResult","Upload Successful!")
        return
    def put_func():
        print("in put func")
        file = filedialog.askopenfilename(initialdir=path.dirname(__file__))
        filename=file.split('/')
        print(filename[-1])
        put_UDP(filename[-1])
        return
    def get_UDP(inputFile):
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
        print(inputFile)
        return
    def get_func():
        print("in get func")
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket1.connect((HOST, PORT))
        instruction = 'lsd'
        temp = instruction+"##"+"\\\\"
        socket1.send(temp.encode())
        socket1.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0',PORT))
        files =(sock.recv(1000).decode()).split(",")
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



lab1 = Label(main, text='Welcome to UTransfer!', font=('times new roman',30), bg="white",fg="green")
lab1.grid(column=1, row=0)

lab1 = Label(main, text='', bg="white")
lab1.grid(column=0,row=1)

lab2 = Label(main, text='Click here for TCP Transfer:', fg="green", bg="white", font=('times new roman',15))
lab2.grid(column=0, row=2)

TCPbutton = Button(main, text="TCP", bg="white", font=('times new roman',10), fg="black",command=lambda:TCPfunc(), padx=15, pady=10)
TCPbutton.grid(column=1, row=2)

lab3 = Label(main, text='',bg="white")
lab3.grid(column=1,row=3)

lab4 = Label(main, text='Click here for UDP Trasnfer:', fg="green", bg="white", font=('times new roman',15))
lab4.grid(column=0, row=4)

UDPbutton = Button(main, text="UDP",bg="white", fg="black",font=('times new roman',10),command=lambda:UDPfunc(), padx=15, pady=10)
UDPbutton.grid(column=1, row=4)

HOST = '192.168.0.116'   
PORT = 32020

#create UDP socket to agree on protocol
socketTemp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


main.mainloop()