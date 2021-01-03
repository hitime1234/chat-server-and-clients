import concurrent.futures
import socket, time

def createnewconvo(name,contact,ss):
    try:      
        f = open(str(name + contact + ".chat"),"w")
        f.write("\n")
        ss.send(b"new file made")
        f.close()
    except:
        return "Error"

def returner(name,ss):
    contact = str((ss.recv(1024)).decode())
    ss.send(b"attempting to get contact data")
    try:
        try:
            f = open(str(name + contact + ".chat"),"r")
            sendablebytes = str(f.read())
            sendablebytes = sendablebytes.encode()
            time.sleep(1)
            ss.send(sendablebytes)
            f.close()
            return True
        except:
            f = open(str(contact + name + ".chat"),"r")
            sendablebytes = str(f.read())
            sendablebytes = sendablebytes.encode()
            time.sleep(1)
            ss.send(sendablebytes)
            f.close()
            return True
    except:
        time.sleep(1)
        ss.send(b"you have no active chain messages with that contact. Creating new chain.")
        choice = str(ss.recv(1024).decode())
        if choice == "yes":
            ret = createnewconvo(name, contact, ss)
            if ret == "error":
                return False
            else:
                return False
        else:
            return False

def sender(name,ss):
    contact = str((ss.recv(1024)).decode())
    message = ss.recv(1024).decode()
    ss.send(b"attempting to send contact message data")
    try:
        try:
            f = open(str(name + contact + ".chat"),"r")
            f.close()
            f = open(str(name + contact + ".chat"),"a")
            f.write(str(name) + " says: \n")
            f.write(str(message))
            f.write("\n")
            f.close()
            ss.send(b"successfully sent")
            return True
        except:
            f = open(str(contact + name + ".chat"),"r")
            f.close()
            f = open(str(contact + name + ".chat"),"a")
            f.write(str(name) + " says: \n")
            f.write(str(message))
            f.write("\n")
            f.close()
            ss.send(b"successfully sent")
            return True   
    except:
        ss.send(b"you have no active chain messages with that contact. Creating new chain.")
        choice = str(ss.recv(1024).decode())
        if choice == "yes":
            ret = createnewconvo(name, contact, ss)
            if ret == "error":
                return False
            else:
                return False
        else:
            return False

def closesocket(ss):
    ss.shutdown(SHUT_RDWR)
    ss.close()


def requesthandler(ss):
    ss.send(b"login needed by user")
    run  = True
    while run == True:
        run2 = True
        while run2 == True:
            try:
                choice2 = (int((ss.recv(1024)).decode()))
                run2 = False
                ss.send(b"int accepted")
            except:
                ss.send(b"must be int")
        if choice2  == 1:
            user = str((ss.recv(1024)).decode())
            pss = str((ss.recv(1024)).decode())
            result = userloginsignup(ss,user,pss)
        elif choice2  ==  2:
            user = "sign"
            pss = "up"
            result = userloginsignup(ss,user,pss)
            if result != False:
                try:
                    user = result[0]
                    pss = result[1]
                    result = True
                except:
                    result =  False
                
        if result == True:
            run == False
            ss.send(b"login success")
            run2 = False
            run  = False
        else:
            ss.send(b"login failure")
            import time
            time.sleep(5)

    


    run3 = True
    while run3 == True:
        choice = str((ss.recv(1024)).decode())
        if choice == "1":
            recvcheck = returner(user, ss)
            if recvcheck != True:
                ss.send(b"unable to get data.. Try again later with the correct/different contact")
        if choice == "2":
            recvcheck = sender(user, ss)
            if recvcheck != True:
                ss.send(b"unable to send the data..  Try again later with the correct/different contact")
        if choice == "3":
            closesocket(ss)
            run3 = False
                       
        
                   
def userloginsignup(ss,user,pss):
    if user == "sign" and pss == "up":
        user = str(ss.recv(1024).decode())
        pss = str(ss.recv(1024).decode())
        try:
            f = open(user + ".login","r")
            f.close()
            return False
        except:
            try:
                f = open(user + ".login","w")
                f.write(str(pss))
                f.close()
                return [user,pss]
            except:
                return False
    else:
        try:
            f = open(user + ".login","r")
            psc = str(f.readline())
            f.close()
            if psc != pss:
                return False
            else:
                return True
        except:
            return False    
        

from requests import get
ip = get('https://api.ipify.org').text
print('My public IP address is: {}'.format(ip))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket. gethostname()
local_ip = socket. gethostbyname(hostname)
hostip = local_ip 
hostport = 25565
server.bind((hostip,hostport))
print("server ready!")
print("address: " + hostip + ":" +str(25565))
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    while True:
        server.listen(10)
        conn, addr = server.accept()
        print("someone connected adding to thread " +  str(addr))
        try:
            executor.submit(requesthandler,conn)
        except:
            print("no spaces left")
            server.close()
                
    
