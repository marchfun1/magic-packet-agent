import socket
import time

# 設定全域字典來追蹤每個來源 IP 位址和封包的接收時間
last_received = {}

def is_magic_packet(packet):
    """檢查封包是否符合 Magic Packet 格式"""
    if len(packet) < 102:
        return False
    if packet[:6] != b'\xff' * 6:
        return False
    return True

def forward_magic_packet(sock, packet, addr):
    """使用單一的套接字將 Magic Packet 轉送到區域網路的廣播位址五次，僅列印一次訊息"""
    broadcast_ip = '255.255.255.255'  # 廣播位址
    target_port = 9
    for _ in range(5):  # 重複發送五次
        sock.sendto(packet, (broadcast_ip, target_port))
    print(f"Forwarded Magic Packet from {addr} 5 times")

def main():
    listen_ip = '0.0.0.0'
    listen_port = 9  # 通常 Magic Packet 使用端口 9

    print("Program started, listening for Magic Packets...")

    # 建立一個用於接收封包的套接字
    sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_receive.bind((listen_ip, listen_port))

    # 建立一個用於轉送封包的套接字並啟用廣播
    sock_forward = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_forward.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        packet, addr = sock_receive.recvfrom(1024)
        current_time = time.time()

        # 檢查封包是否為 Magic Packet
        if not is_magic_packet(packet):
            print(f"Ignored non-Magic Packet from {addr}")
            continue

        # 確認 20 秒內沒有接收到相同的封包
        if addr in last_received:
            last_time, last_packet = last_received[addr]
            time_since_last_packet = current_time - last_time
            if time_since_last_packet < 20 and packet == last_packet:
                print(f"Ignored duplicate Magic Packet from {addr}, received {time_since_last_packet:.2f} seconds ago")
                continue

        # 更新接收時間和封包內容，並使用固定的套接字轉送封包五次
        last_received[addr] = (current_time, packet)
        forward_magic_packet(sock_forward, packet, addr)

if __name__ == "__main__":
    main()