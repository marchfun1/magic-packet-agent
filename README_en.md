# Magic Packet Agent

[中文](./README.md)

This project is specifically designed for remote wake-on-LAN operations for computers in a home or company local area network. Install this program on a Linux machine within the LAN to serve as a relay station for the magic packet.

## Setup Steps

1. A Linux system within the LAN needs to install this program
2. Requires Python 3 (this program will automatically install it)
3. Needs the front-end router to forward UDP port 9 to the Linux system
4. Open firewall port 9

## Installation Guide

If git is not installed in the system, you need to use the following command to install it:

```bash
sudo apt install git
```

**Installation Commands (execute in order):**

```bash
git clone https://github.com/marchfun1/magic-packet-agent.git
cd magic-packet-agent
chmod +x install.sh
sudo ./install.sh
```

The program will be installed as a system service.

## Changelog

### v2.0.0 (2026-04-06)

- **Security Optimization**: Added DoS memory exhaustion protection with cache limits.
- **Privilege Dropping**: Implemented `DynamicUser` and `CAP_NET_BIND_SERVICE` to avoid running as root.
- **Logic Correction**: Switched to MAC address-based packet identification to eliminate broadcast loops and network storms.
- **Performance Improvement**: Added automatic cleanup for expired cache to prevent memory leaks.
- **Installation Optimization**: Scripts are now fully non-interactive, suitable for automated deployment.
- **Language Splitting**: Split README into separate Chinese and English versions.

### v1.0.0 (Initial Version)

- Basic Magic Packet listening and broadcast relaying.
- Standard systemd service support.

---

**Author Information**

- Author: 域創數位工作室 (LOCALSOFT Digital Studio)
- Website: <https://suma.tw>
