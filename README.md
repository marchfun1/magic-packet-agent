# Magic Packet Agent (魔術封包轉送站)

[English](./README_en.md)

本專案專門針對有需要在遠端將家中或公司內區域網路電腦進行遠端喚醒的作業。利用在區域網路中的 Linux 安裝本程式以作為 magic packet (魔術封包) 的轉送站。

## 建置步驟

1. 在區域網路內部其中一部 Linux 上安裝本程式
2. 需要 python 3 (若未安裝則本程式會自動安裝)
3. 需要前端路由器轉送 UDP 埠號 9 到該 Linux
4. 開放防火牆埠號 9

## 安裝指南

若系統中尚未安裝 git 則需使用以下指令安裝：

```bash
sudo apt install git
```

**安裝指令 (依序執行)：**

```bash
git clone https://github.com/marchfun1/magic-packet-agent.git
cd magic-packet-agent
chmod +x install.sh
sudo ./install.sh
```

即可安裝為系統服務。

## 更新日誌

### v2.0.0 (2026-04-06)

- **安全性優化**：新增阻斷服務攻擊 (DoS) 記憶體耗盡防護，限制快取上限。
- **權限降級**：採用 `DynamicUser` 與 `CAP_NET_BIND_SERVICE` 運行服務，避免以 root 權限執行。
- **邏輯修正**：改以 MAC 位址進行重複封包識別，徹底解決廣播迴圈造成的網路風暴。
- **效能改進**：新增過期快取自動清理機制，防止記憶體洩漏。
- **安裝優化**：腳本改為完全非互動式，適合自動化部署。
- **語系拆分**：將 README 拆分為獨立的中、英文版本。

### v1.0.0 (初期版本)

- 基本的 Magic Packet 監聽與廣播轉發功能。
- 基礎 systemd 服務腳本。

---

**作者資訊**

- 作者：域創數位工作室 (LOCALSOFT Digital Studio)
- 網址：<https://suma.tw>
