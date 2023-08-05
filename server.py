import socket
from modules.player import Player
from modules.receivable_packet import *
from modules.sendable_packet import *
import datetime

# 1δlwekjfkewj▼
# δlwekjfkewj
# 0δlwekjfkewjδlwekjfkewjδlwekjfkewjδlwekjfkewj▼

observable_player = None

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen()

player_list = [Player(server_socket)]

sendable_packets = []
players_to_remove = []

def process_packet(packet, player):
    observable_player = player
    match packet.receivable_packet_type:
        case ReceivablePacketType.LOGIN.value:
            exists = False
            for player in player_list:
                if player.name != None:
                    if player.name == packet.receivable_packet_data[0]:
                        exists = True
                        break
            if exists:
                packet_to_send = SendablePacket(SendablePacketType.ERROR, "Error, name exists")
                observable_player.connection_handler.send_packet(packet_to_send)
                observable_player.connection_handler.connected = False
            else:
                observable_player.set_name(packet.receivable_packet_data[0])
                observable_player.append_packet(SendablePacket(SendablePacketType.SUCCESSFULL_LOGIN, observable_player.name))
        
        case ReceivablePacketType.UPDATE_POSITION.value:
            player.updatePosition(float(packet.receivable_packet_data[0]), float(packet.receivable_packet_data[1]), float(packet.receivable_packet_data[2]))

print("Running Server\n")
delta = datetime.timedelta(milliseconds=20)
now = datetime.datetime.now()
nextLoop = datetime.datetime.now() + delta
while True:
    if player_list[-1].client_socket != None:
        player_list.append(Player(server_socket))
    for player in player_list:
        if not player.connection_handler.connected:
            players_to_remove.append(player)
        if player.client_socket != None and player.connection_handler.connected:
            while player.connection_handler.received_packets:
                packet = player.connection_handler.received_packets.pop()
                process_packet(packet, player)
            while player.connection_handler.sendable_packets:
                packet = player.connection_handler.sendable_packets.pop()
                player.connection_handler.send_packet(packet)
            player.append_packet(SendablePacket(SendablePacketType.SYNC_PLAYERS, [f"{p.name}{END_OF_PACKET_TYPE}{p.x}{END_OF_PACKET_TYPE}{p.y}{END_OF_PACKET_TYPE}{p.vx}" if p.name != None else None for p in player_list]))
    for player in players_to_remove:
        player.connection_handler.disconnect()
        player_list.remove(player)
    players_to_remove = []
    while(now < nextLoop):
        now = datetime.datetime.now()
    nextLoop = datetime.datetime.now() + delta
