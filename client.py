#client
import socket, time
def auth(ss):
    print("")
    print("server: " + str(ss.recv(1024).decode()))
    print("\n\n")
    runauth = True
    while runauth == True:
        run = True
        while run == True:
            try:
               choice = int(input("1.login\n2.signup\n> "))
               if choice == 1 or choice == 2:
                   run = False
               else:
                    print("\nmust be 1 or 2")
            except:
                print("\nmust be 1 or 2")

        if choice == 1:
            time.sleep(1)
            ss.send(b"1")
            hold = ss.recv(1024)
            hold = ""
            time.sleep(1)
            user = input("what is the username of the account you want to login with? ")
            pss = input("what is the password of the account? ")
            print("\nthis will take 3 seconds")
            usend = user.encode()
            psend = pss.encode()
            time.sleep(1)
            ss.send(usend)
            time.sleep(1)
            ss.send(psend)
            time.sleep(1)
            success_maybe = str(ss.recv(1024).decode())
            if success_maybe == "login success":
                print("\naccount accepted.")
                runauth = False
            else:
                print("\naccount is not accepted to be logged into.\n this could be due to bad login file or wrong username/password.")
        elif choice == 2:
            time.sleep(1)
            ss.send(b"2")
            hold = ss.recv(1024)
            hold = ""
            time.sleep(1)
            user = input("what is the username of the account you want to create? ")
            pss = input("what will the password of the account be? ")
            print("\nthis will take 3 seconds")
            usend = user.encode()
            psend = pss.encode()
            time.sleep(1)
            ss.send(usend)
            time.sleep(1)
            ss.send(psend)
            time.sleep(1)
            success_maybe = str(ss.recv(1024).decode())
            if success_maybe == "login success":
                print("\naccount accepted and now stored.")
                runauth = False
            else:
                print("\naccount is not accepted to be signed up with.\n this could be due to bad characters in username/password or someone already having the username.")
    menu(ss)
    
def returna(ss):
    print("")
    print("\nnote your contact is someone how you have active message chain on a server with.\nif you don't have one registered with chat you can create a new chain.\n")
    contactuser = input("what is your contact's username so the server can find the messages? ")
    time.sleep(1)
    ss.send(contactuser.encode())
    print("server: " + (str(ss.recv(1024).decode())))
    time.sleep(1)
    errorcheck = (str(ss.recv(1024).decode()))
    time.sleep(1)
    if errorcheck == "you have no active chain messages with that contact. Creating new chain.":
        print("server: " + errorcheck)
        print("to agree to this say yes")
        arge = input("are you sure? ")
        time.sleep(1)
        if arge == "yes":
            ss.send(arge.encode())
            return "Falseyes"
        elif arge != "":
            ss.send(arge.encode())
            return False
        else:
            arge = "error"
            ss.send(arge.encode())
            return False
    else:
        print("chain message to and from " + str(contactuser) + ":\n\n " + errorcheck)
        return True
        

def send(ss):
    print("")
    print("\nnote your contact is someone how you have active message chain on a server with.\nif you don't have one registered with chat you can create a new chain.\n")
    contactuser = input("what is your contact's username so the server can find the messages? ")
    messageforcontact = input("what is the message for the contact? \n> ")
    time.sleep(1)
    ss.send(contactuser.encode())
    time.sleep(1)
    ss.send(messageforcontact.encode())
    print("server: " + (str(ss.recv(1024).decode())))
    errorcheck = (str(ss.recv(1024).decode()))
    print("server: " + errorcheck)
    if errorcheck == "you have no active chain messages with that contact. Creating new chain.":
        print("to agree to this say yes")
        arge = input("are you sure? ")
        time.sleep(1)
        if arge == "yes":
            ss.send(arge.encode())
            return "Falseyes"
        elif arge != "":
            ss.send(arge.encode())
            return False
        else:
            arge = "error"
            ss.send(arge.encode())
            return False
    
def menu(ss):
    run = True
    runmenu = True
    while runmenu  ==  True:
        run = True
        while run == True:
            try:
               choice = int(input("\n1.receive contact chat messages\n2.send message to contact\n3.close server connection\n> "))
               if choice == 1 or choice == 2 or choice == 3:
                   run = False
               else:
                    print("\nmust be 1 or 2 or 3")
            except:
                print("\nmust be 1 or 2 or 3")


            sendchoice = str(choice).encode()
            ss.send(sendchoice)
            if choice == 1:
                check = returna(ss)
                if check == False:
                    print("server: " + str((ss.recv(1024)).decode()))
                if check == "Falseyes":
                    print("server: " + str((ss.recv(1024)).decode()))
                    ss.recv(1024).decode()
            if choice  == 2:
                check = send(ss)
                if check == False:
                    print("server: " + str((ss.recv(1024)).decode()))
                if check == "Falseyes":
                    print("server: " + str((ss.recv(1024)).decode()))
                    ss.recv(1024).decode()
            if choice == 3:
                time.sleep(1)
                runmenu = False
                

def createconnection():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostip = input("what is the hostname/ip address of the server chat you want to connect to? ")
    hostport = int(input("what is the port of the server you want to connect to default is 25565? "))
    client.connect((hostip,hostport))
    auth(client)

def main():
    try:
        createconnection()
    except:
        print(("\n" * 5) + "connection closed" + "\n\n")
        main()

main()
    
