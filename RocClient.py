import xml.etree.ElementTree as ET

class RocClient:

    def __init__(self, socket):
        self.socket = socket
        self.id = "central,"
        self.buffer = ""

    def setId(self, id):
        self.id = id
    
    def recv(self):
        cmds = []
        try:
            data = self.socket.recv(4096).decode("utf-8")
            if not data:
                return False
            else:
                for char in data:
                    if char == '\n':
                        cmds.append(ET.fromstring(self.buffer))
                        self.buffer = ""
                    else:
                        self.buffer += char
                return cmds
        except Exception as e:
            print("[INFO] Client recv error")
            return False
        

    def send(self, data):
        self.socket.send(data)
    
    def close(self):
        self.socket.close()