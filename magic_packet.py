import socket
import time

DEDUP_WINDOW_SECONDS = 20
MAX_RECENT_MACS = 1000

GLOBAL_RATE_PER_SECOND = 10.0
GLOBAL_RATE_BURST = 20.0
SOURCE_RATE_PER_SECOND = 2.0
SOURCE_RATE_BURST = 5.0
MAX_SOURCE_BUCKETS = 2048
SOURCE_BUCKET_TTL_SECONDS = 60
RATE_LIMIT_LOG_INTERVAL_SECONDS = 5

# 設定全域字典來追蹤每組 MAC 位址封包的接收時間
last_received = {}
source_buckets = {}
global_bucket = {"tokens": GLOBAL_RATE_BURST, "updated_at": time.monotonic()}
last_rate_limit_log = {}

def is_magic_packet(packet):
    """檢查封包是否符合 Magic Packet 格式"""
    if len(packet) not in (102, 108):
        return False
    if packet[:6] != b'\xff' * 6:
        return False

    mac = packet[6:12]
    return packet[6:102] == mac * 16

def refill_bucket(bucket, now, rate_per_second, burst):
    elapsed = max(0.0, now - bucket["updated_at"])
    bucket["tokens"] = min(burst, bucket["tokens"] + elapsed * rate_per_second)
    bucket["updated_at"] = now

def cleanup_source_buckets(now):
    expired_sources = [
        source_ip
        for source_ip, bucket in source_buckets.items()
        if now - bucket["updated_at"] > SOURCE_BUCKET_TTL_SECONDS
    ]
    for source_ip in expired_sources:
        del source_buckets[source_ip]

def allow_packet(source_ip, now):
    """套用全域與來源 IP token bucket rate limit。"""
    cleanup_source_buckets(now)

    refill_bucket(global_bucket, now, GLOBAL_RATE_PER_SECOND, GLOBAL_RATE_BURST)
    if global_bucket["tokens"] < 1:
        return False, "global"

    source_bucket = source_buckets.get(source_ip)
    if source_bucket is None:
        if len(source_buckets) >= MAX_SOURCE_BUCKETS:
            return False, "source-cache-full"
        source_bucket = {"tokens": SOURCE_RATE_BURST, "updated_at": now}
        source_buckets[source_ip] = source_bucket

    refill_bucket(source_bucket, now, SOURCE_RATE_PER_SECOND, SOURCE_RATE_BURST)
    if source_bucket["tokens"] < 1:
        return False, "source"

    global_bucket["tokens"] -= 1
    source_bucket["tokens"] -= 1
    return True, None

def log_rate_limit_drop(addr, reason, now):
    last_log_time = last_rate_limit_log.get(reason, 0)
    if now - last_log_time < RATE_LIMIT_LOG_INTERVAL_SECONDS:
        return
    last_rate_limit_log[reason] = now
    print(f"Dropped rate-limited packet from {addr}: {reason}")

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

        current_time = time.monotonic()
        allowed, reason = allow_packet(addr[0], current_time)
        if not allowed:
            log_rate_limit_drop(addr, reason, current_time)
            continue

        # 檢查封包是否為 Magic Packet
        if not is_magic_packet(packet):
            print(f"Ignored non-Magic Packet from {addr}")
            continue

        # 清理超過 20 秒的歷史紀錄以避免記憶體洩漏
        keys_to_delete = [k for k, v in last_received.items() if current_time - v[0] > DEDUP_WINDOW_SECONDS]
        for k in keys_to_delete:
            del last_received[k]

        # 擷取 Magic Packet 中的 MAC 位址部分用作防重的識別
        mac_addr = packet[6:12]
        mac_hex = ':'.join(f'{b:02x}' for b in mac_addr)

        # 防止攻擊者用隨機 MAC 撐爆快取；滿了就拒絕新的 MAC，不清空既有保護狀態。
        if mac_addr not in last_received and len(last_received) >= MAX_RECENT_MACS:
            print(f"Dropped Magic Packet for MAC {mac_hex} from {addr}: MAC cache is full")
            continue

        # 確認 20 秒內沒有接收到相同 MAC 的封包
        if mac_addr in last_received:
            last_time, _ = last_received[mac_addr]
            time_since_last_packet = current_time - last_time
            if time_since_last_packet < DEDUP_WINDOW_SECONDS:
                print(f"Ignored duplicate Magic Packet for MAC {mac_hex} from {addr}, received {time_since_last_packet:.2f} seconds ago")
                continue

        # 更新接收時間，並轉送封包
        last_received[mac_addr] = (current_time, packet)
        print(f"Received valid Magic Packet for MAC {mac_hex} from {addr}")
        forward_magic_packet(sock_forward, packet, addr)

if __name__ == "__main__":
    main()
