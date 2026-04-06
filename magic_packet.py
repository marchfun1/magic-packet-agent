import socket
import time

# 設定全域字典來追蹤每組 MAC 位址封包的接收時間
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
        try:
            sock.sendto(packet, (broadcast_ip, target_port))
        except Exception as e:
            print(f"Error forwarding packet: {e}")
            break
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
        try:
            packet, addr = sock_receive.recvfrom(1024)
        except Exception as e:
            print(f"Error receiving packet: {e}")
            continue

        current_time = time.time()

        # 檢查封包是否為 Magic Packet
        if not is_magic_packet(packet):
            print(f"Ignored non-Magic Packet from {addr}")
            continue

        # 清理超過 20 秒的歷史紀錄以避免記憶體洩漏
        keys_to_delete = [k for k, v in last_received.items() if current_time - v[0] > 20]
        for k in keys_to_delete:
            del last_received[k]

        # 防護措施：限制字典大小，防止攻擊者發送隨機 MAC 位址導致記憶體耗竭 (DoS)
        if len(last_received) > 1000:
            print("Security Warning: MAC address cache exceeded limit due to flood. Flushing cache.")
            last_received.clear()

        # 擷取 Magic Packet 中的 MAC 位址部分用作防重的識別
        mac_addr = packet[6:12]
        mac_hex = ':'.join(f'{b:02x}' for b in mac_addr)

        # 確認 20 秒內沒有接收到相同 MAC 的封包
        if mac_addr in last_received:
            last_time, _ = last_received[mac_addr]
            time_since_last_packet = current_time - last_time
            if time_since_last_packet < 20:
                print(f"Ignored duplicate Magic Packet for MAC {mac_hex} from {addr}, received {time_since_last_packet:.2f} seconds ago")
                continue

        # 更新接收時間，並轉送封包
        last_received[mac_addr] = (current_time, packet)
        print(f"Received valid Magic Packet for MAC {mac_hex} from {addr}")
        forward_magic_packet(sock_forward, packet, addr)

if __name__ == "__main__":
    main()