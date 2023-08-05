from .connection_handler import *


class Player:
    def __init__(self, server_socket):
        self.client_socket = None
        self.name = None
        self.connection_handler = ConnectionHandler(self, server_socket)
        self.connection_handler.start()
        self.x = 0
        self.y = 0
        self.vx = 0
    
    def updatePosition(self, x, y, vx):
        self.x = x
        self.y = y
        self.vx = vx

    def set_name(self, name):
        self.name = name
    
    def append_packet(self, packet):
        self.connection_handler.append_packet(packet)