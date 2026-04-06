# Magic Packet Agent

[中文](./README.md)

This project is specifically designed to facilitate remote Wake-on-LAN operations for computers inside a home or office local area network (LAN). By installing this agent on a Linux machine (e.g., Raspberry Pi, old computer, or server) within the LAN, it serves as a **Magic Packet Relay Station** between external requests and your internal network devices.

## Key Features

- **Efficient Proxy Relay**: Intercepts external WOL requests and re-broadcasts them specifically within the target LAN.
- **Intelligent Anti-Loopback**: Employs a MAC address-based deduplication algorithm to eliminate network storms and infinite broadcast loops.
- **Enhanced Security Armor**:
    - **DoS Protection**: Includes automatic memory cache clearing to protect against malicious UDP flooding.
    - **Privilege Dropping**: Runs under systemd `DynamicUser` sandbox with `CAP_NET_BIND_SERVICE`, allowing secure listening on Port 9 without root privileges.
- **Ultra-Lightweight Implementation**: Pure Python, zero dependencies, minimal CPU and memory footprint.
- **One-Click Silent Install**: Optimized shell script supports non-interactive mode, perfect for automated deployment or scripting.

## How It Works

1. **Listen**: The daemon listens for incoming packets on UDP Port 9.
2. **Verify**: Once a packet is received, it validates it against the standard Magic Packet specification (FFx6 + MACx16).
3. **Filter**: The agent extracts the destination MAC address and checks its recent history. If a duplicate wake request for the same MAC is received within 20 seconds, it is ignored to save bandwidth.
4. **Re-broadcast**: Valid packets are re-encapsulated and broadcasted to `255.255.255.255` on the local network to wake the sleeping device.

## Setup Steps

1. Install this agent on a Linux system within the LAN.
2. Ensure Python 3 is installed (the `install.sh` script will attempt to install it if missing).
3. On your primary router, configure **Port Forwarding**: Forward external UDP Port 9 to the local IP of this agent.
4. Ensure your Linux firewall (ufw, iptables) allows incoming traffic on UDP Port 9.

## Installation Guide

If `git` is not installed on your system, please run:

```bash
sudo apt-get update && sudo apt-get install -y git
```

**Quick Install Commands (run with root or sudo):**

```bash
git clone https://github.com/marchfun1/magic-packet-agent.git
cd magic-packet-agent
chmod +x install.sh
sudo ./install.sh
```

Upon completion, the system will automatically start the `forward_magic_packet.service` daemon.

## Changelog

### v2.0.0 (2026-04-06)

- **Security Optimization**: Added DoS memory exhaustion protection with cache limits.
- **Privilege Dropping**: Implemented `DynamicUser` and `CAP_NET_BIND_SERVICE` for enhanced execution safety.
- **Logic Correction**: Switched to MAC address-based identification to eliminate broadcast loops and network storms.
- **Performance Improvement**: Added automatic cache cleanup to prevent memory leaks.
- **Installation Optimization**: Scripts are now fully non-interactive for better deployment.

### v1.0.0 (Initial Version)

- Basic Magic Packet listening and broadcast relaying.
- Standard systemd service support.

---

**Author Information**

- Author: 域創數位工作室 (LOCALSOFT Digital Studio)
- Website: <https://suma.tw>
