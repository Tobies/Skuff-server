import enum
from .constants import *


class SendablePacketType(enum.Enum):
    ERROR = 0
    SUCCESSFULL_LOGIN = 1
    SYNC_PLAYERS = 2


class SendablePacket:
    def __init__(self, packet_type, packet_data):
        self.packet_type = packet_type
        self.packet_data = packet_data

    def format_packet(self):
        if type(self.packet_data) == str:
            return f"{self.packet_type.value}{END_OF_PACKET_TYPE}{self.packet_data}{END_OF_PACKET_DATA}"
        elif type(self.packet_data) == list:
            buffer = ""
            for data in self.packet_data:
                if data != None:
                    buffer += data
                    buffer += END_OF_PACKET_TYPE
            return f"{self.packet_type.value}{END_OF_PACKET_TYPE}{buffer}{END_OF_PACKET_DATA}"
        else:
            print("bad packet !!(sendable_packet.py )")
