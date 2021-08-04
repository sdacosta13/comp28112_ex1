import im
from time import sleep
server = im.IMServerProxy('https://web.cs.manchester.ac.uk/p11469sd/comp28112_ex1/IMserver.php')


class User:
    def __init__(self, server, name):
        self.server = server
        self.name = name


class UserA(User):
    def __init__(self, server, name):
        super().__init__(server,name)
        self.server["aConnected"] = "true"
        self.server["control"] = "a"
        self.server["userAname"] = name
        read = True
        while(True):
            if(self.server["control"] == b"a\n" and read):
                print(self.name, end="")
                msg = input(" >> ")
                self.server["msg"] = msg
                self.server["sent"] = "true"
                read = False
            elif(not read and self.server["control"] == b"b\n" and self.server["sent"] == b"true\n"):
                print(self.server["userBname"].decode("utf-8")[:-1], end="")
                print(" >> ", end = "")
                print(self.server["msg"].decode("utf-8"), end="")
                self.server["sent"] = "false"
                read = True
                self.server["control"] = "a"
            sleep(0.1)


def reset():
    server.clear()
    server["aConnected"] = "false"
    server["bConnected"] = "false"
    server["control"] = "a"
    server["msg"] = ""
    server["sent"] = "false"
    del server["userAname"]
    del server["userBname"]

class UserB(User):
    def __init__(self, server, name):
        super().__init__(server,name)
        self.server["bConnected"] = "true"
        self.server["control"] = "a"
        self.server["userBname"] = name
        read = False
        while(True):
            if(self.server["control"] == b"b\n" and read):
                print(self.name, end="")
                msg = input(" >> ")
                self.server["msg"] = msg
                self.server["sent"] = "true"
                read = False
            elif(not read and self.server["control"] == b"a\n" and self.server["sent"] == b"true\n"):
                print(self.server["userAname"].decode("utf-8")[:-1], end="")
                print(" >> ", end = "")
                print(self.server["msg"].decode("utf-8"), end="")
                self.server["sent"] = "false"
                read = True
                self.server["control"] = "b"
            sleep(0.1)

name = input("Name: ")
try:
    if((server["aConnected"] == b"true\n") and (server["bConnected"] == b"false\n")):
        user = UserB(server, name)
    elif((server["aConnected"] == b"false\n") and (server["bConnected"] == b"true\n")):
        user = UserA(Server, name)
    elif((server["aConnected"] == b"false\n") and (server["bConnected"] == b"false\n")):
        user = UserA(server, name)
    else:
        reset()
        print("A failure has occured")
except KeyboardInterrupt:
    reset()
