import socket
import time

def forward_magic_packet(sock, packet):
    broadcast_ip = '255.255.255.255'  # 廣播位址
    target_port = 9

    try:
        sock.sendto(packet, (broadcast_ip, target_port))
        print(f"Packet forwarded to {broadcast_ip}:{target_port}")
    except socket.error as e:
        print(f"Error sending packet: {e}")

def main():
    listen_ip = '0.0.0.0'
    listen_port = 9  # 通常 Magic Packet 使用埠 9

    # 建立接收封包的通訊端
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_sock.bind((listen_ip, listen_port))

    # 建立廣播通訊端
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    last_packet = None

    try:
        print("Listening for Magic Packets...")
        while True:
            # 接收封包
            packet, addr = recv_sock.recvfrom(1024)
            
            # 篩選重複的 Magic Packet
            if packet != last_packet and is_magic_packet(packet):
                print(f"Received Magic Packet from {addr}")
                forward_magic_packet(send_sock, packet)
                last_packet = packet
            else:
                print(f"Ignored non-magic packet from {addr}")

            # 增加一點延遲來避免高 CPU 使用率
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting...")
    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        recv_sock.close()
        send_sock.close()

def is_magic_packet(packet):
    # 檢查封包是否是 Magic Packet
    if len(packet) >= 102:
        # Magic Packet 是一個 6-byte FF 和 16 個重複的 MAC 位址
        return packet[:6] == b'\xff' * 6
    return False

if __name__ == "__main__":
    main()
