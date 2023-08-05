import enum


class ReceivablePacketType(enum.Enum):
    LOGIN = 0
    UPDATE_POSITION = 1


class ReceivablePacket:
    def __init__(self, x):
        self.receivable_packet_type = int(x[0])
        self.receivable_packet_data = x[1:]
