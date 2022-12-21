import socket
import struct

# Cria um socket UDP
udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Vincula o socket a um endereço IP e porta
udp_socket.bind(("0.0.0.0", 5606))
print('porta aberta 5606')
try:
    while True:
        # Lê um pacote UDP e obtém o endereço do cliente que o enviou
        data, client_address = udp_socket.recvfrom(1024)
        
        
        # Desempacota os dados usando o formato esperado pelo jogo Project CARS 2
        (header, packet_number, packet_size, packet_type, packet_version, packet_tick, packet_session_uid,
        packet_frame_identifier, packet_player_car_index, packet_yaw, packet_pitch, packet_roll,
        packet_x_local_velocity, packet_y_local_velocity, packet_z_local_velocity,
        packet_susp_acceleration_x, packet_susp_acceleration_y, packet_susp_acceleration_z,
        packet_ang_acceleration_x, packet_ang_acceleration_y, packet_ang_acceleration_z,
        packet_long_acceleration, packet_lat_acceleration, packet_vert_acceleration, packet_velocity_x,
        packet_velocity_y, packet_velocity_z, packet_ang_velocity_x, packet_ang_velocity_y, packet_ang_velocity_z,
        packet_acc_g_force_x, packet_acc_g_force_y, packet_acc_g_force_z) = struct.unpack("!LHHHHLLQLfffffffffffffffffffffffff", data)
        
        # Imprime alguns dos dados lidos
        print(f"Pitch: {packet_pitch}")
        print(f"Roll: {packet_roll}")
        print(f"Longitudinal acceleration: {packet_long_acceleration}")
        print(f"Lateral acceleration: {packet_lat_acceleration}")
except KeyboardInterrupt:
    pass   