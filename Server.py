import socket, select
import xml.etree.ElementTree as ET
from RocClient import RocClient
import threading

class RocServer:
    def __init__(self, host, port):
        print("[INFO] Create server on port " + str(port))
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Réutiliser l'adresse
        print("[INFO] binding on port " + str(port))
        self.serverSocket.bind((host, port))
        print("[INFO] listen on port " + str(port))
        self.serverSocket.listen(port)
        print("[INFO] Waiting from new connection")
        self.rocClients = []

    def handle_client(self, client):
        while True:
            data = client.recv()
            if data == False:
                break
            else:
                try:
                    for cmd in data:
                        if (cmd.tag == "setId"):
                            client.setId(cmd.attrib["id"])
                            print("[INFO] Identification of client " + client.id)
                        else:
                            if ("central" in client.id):
                                if ("id" in cmd.attrib):
                                    print("[INFO] New central message for id " + cmd.attrib["id"])
                                    clientsTo = self.getClientById(cmd.attrib["id"])
                                elif ("uidname" in cmd.attrib):
                                    print("[INFO] New central message for uidname " + cmd.attrib["uidname"])
                                    clientsTo = self.getClientById(cmd.attrib["uidname"])
                                else:
                                    print("[INFO] New central : No id ...")
                                    clientsTo = []
                                print("[INFO] Transmit " + ET.tostring(cmd).decode("ascii"))
                                for clients in clientsTo:
                                    clients.send((ET.tostring(cmd).decode() + "\n").encode("ascii"))
                                        #client.send('<fb id="fb1" state="true"/>\n'.encode('ascii'))
                                        #client.send('<fb id="fb1" state="false"/>\n'.encode('ascii'))
                            else:
                                print("[INFO] New message from client " + client.id)
                                clientsTo = self.getClientById("central")
                                for clients in clientsTo:
                                    clients.send((ET.tostring(cmd).decode() + "\n").encode("ascii"))
                except Exception as e:
                    print("[INFO] Client parse error")
                    print(repr(e))
                    break
        print("[INFO] Client " + client.id + " disconnected")
        client.close()
        self.rocClients.remove(client)

    def update(self):
        client, _ = self.serverSocket.accept()
        print("[INFO] New connection from client")
        rocClient = RocClient(client)
        self.rocClients.append(rocClient)
        threading.Thread(target=self.handle_client, args=(rocClient,)).start()
                    

    def getClientFromSocket(self, socket):
        for client in self.rocClients:
            if (client.socket == socket):
                return client
        return

    def getClientById(self, id):
        clients = []
        for client in self.rocClients:
            if ((id + ",") in client.id):
                clients.append(client)
        return clients

    def getAllClientSocket(self):
        clients = []
        for client in self.rocClients:
            clients.append(client.socket)
        return clients

    def close(self):
        for client in self.rocClients:
            client.close()
        self.serverSocket.close()