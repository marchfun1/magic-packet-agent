# Magic Packet Agent (魔術封包轉送站)

[English](./README_en.md)

本專案專門針對有需要在遠端將家中或公司內區域網路電腦進行遠端喚醒的作業。利用在區域網路中的一部 Linux 主機（如樹莓派、舊電腦或伺服器）安裝本程式，作為外部封包與內部區域網路間的 **Magic Packet (魔術封包) 轉送站**。

## 功能特點

- **高效代理轉發**：精準攔截外部喚醒請求，並重新廣播至區域網路所有主機。
- **智能防迴圈機制**：採用 MAC 位址去重算法，徹底杜絕因廣播特性導致的網路風暴與無限迴圈。
- **強化安全防禦**：
    - **DoS 防護**：具備自動記憶體快取清理，防止惡意泛洪攻擊 (UDP Flood)。
    - **最小權限運行**：支援 systemd `DynamicUser` 權限降級，不需 root 帳號即可安全監聽 Port 9。
- **極致輕量化**：基於 Python 原生開發，無需第三方套件，系統資源佔用極低。
- **一鍵全自動安裝**：專門優化的 Shell 腳本支援非互動模式，適合快速部署。

## 工作原理

1. **監聽**：程式在 Linux 背景持續監聽 UDP Port 9。
2. **驗證**：接收到封包後，自動驗證是否符合 Magic Packet 的標準規範（FFx6 + MACx16）。
3. **過濾**：比對 MAC 位址與接收時間，若 20 秒內重複收到相同 MAC 的喚醒請求，將自動過濾以維護網路頻寬。
4. **轉廣發**：將合法的喚醒封包重新封裝並廣播至區域網路 (`255.255.255.255`)，以喚醒目標設備。

## 建置步驟

1. 在區域網路內部其中一部 Linux 上安裝本程式。
2. 系統需具備 Python 3 (若未安裝則 `install.sh` 會嘗試自動安裝)。
3. 在前端路由器（Router）設定 **連接埠轉發 (Port Forwarding)**：將外部 UDP Port 9 轉發至本主機的內部 IP。
4. 確保主機防火牆（如 ufw 或 iptables）已開放 UDP Port 9。

## 安裝指南

若系統中尚未安裝 git，需先執行：

```bash
sudo apt-get update && sudo apt-get install -y git
```

**快速安裝指令 (請以 root 或 sudo 權限執行)：**

```bash
git clone https://github.com/marchfun1/magic-packet-agent.git
cd magic-packet-agent
chmod +x install.sh
sudo ./install.sh
```

安裝完成後，系統會自動啟動名為 `forward_magic_packet.service` 的服務。

## 更新日誌

### v2.0.0 (2026-04-06)

- **安全性優化**：新增阻斷服務攻擊 (DoS) 記憶體耗盡防護，限制快取上限。
- **權限降級**：採用 `DynamicUser` 與 `CAP_NET_BIND_SERVICE` 運行服務，提升安全性。
- **邏輯修正**：改以 MAC 位址進行重複封包識別，解決廣播迴圈造成的網路風暴。
- **效能改進**：新增過期快取自動清理機制，防止記憶體洩漏。
- **安裝優化**：腳本改為完全非互動式，適合自動化部署。

### v1.0.0 (初期版本)

- 基本的 Magic Packet 監聽與廣播轉發功能。
- 基礎 systemd 服務腳本。

---

**作者資訊**

- 作者：域創數位工作室 (LOCALSOFT Digital Studio)
- 網址：<https://suma.tw>
