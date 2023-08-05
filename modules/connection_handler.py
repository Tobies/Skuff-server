import threading
import socket
from .receivable_packet import *
from .constants import *


class ConnectionHandler(threading.Thread):
    def __init__(self, player, server_socket):
        threading.Thread.__init__(self)
        self.server_socket = server_socket
        self.connected = True
        self.sendable_packets = []
        self.received_packets = []
        self.player = player
        self.current_char = ""
        self.current_message = ""
        self.buffer = ""

    def run(self):
        self.client_socket, self.address = self.server_socket.accept()
        self.player.client_socket = self.client_socket
        print(f"{self.address} connected successfully")
        while self.connected:
            try:
                payload = self.client_socket.recv(1024).decode('utf-8')
                if (len(payload) > 0):
                    self.buffer += payload
                    while len(self.buffer) > 0:
                        self.current_char = self.buffer[0]
                        self.buffer = self.buffer[1:]
                        if self.current_char == END_OF_PACKET_DATA:
                            data = self.current_message.split(END_OF_PACKET_TYPE)
                            self.received_packets.append(ReceivablePacket(data))
                            self.current_message = ""
                        else:
                            self.current_message = self.current_message + self.current_char
                else:
                    self.connected = False
                payload = ""
            except (ConnectionResetError, OSError):
                self.connected = False
        print(f"[{self.address}], [{self.player.name}] has disconnected")
    
    def disconnect(self):
        self.connected = False
        self.client_socket.shutdown(socket.SHUT_RDWR)
        self.client_socket.close()
    
    def send_packet(self, packet):
        try:
            if self.connected:
                self.client_socket.send(packet.format_packet().encode('utf-8'))
        except:
            self.connected = False

    def append_packet(self, packet):
        self.sendable_packets.append(packet)
    