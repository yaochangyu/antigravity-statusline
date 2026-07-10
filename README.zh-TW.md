# Antigravity Statusline (繁體中文)

[English](README.md) | [繁體中文](README.zh-TW.md)

這是一個適用於 `antigravity-cli`（及 Claude Code 環境）的自訂 Python 地位列 (Statusline) 腳本。它能即時顯示 Git 分支資訊、API 額度限制、當前累積花費、Session 持續時間以及執行中的 Agent 技能。

![Antigravity Statusline 演示](demo.png)

## 功能特色

- **Git 狀態**：顯示當前分支、變動狀態 (`*`)，以及領先/落後 (ahead/behind) 的 commit 數量。
- **額度限制**：以自訂進度條顯示 5 小時及每週的 API 額度使用量與重置倒數。
- **費用監控**：直接顯示今日與本月的 API 累計花費金額（不使用無謂的每日限制）。
- **真實技能偵測**：動態解析對話紀錄 (Transcript)，僅在載入真實技能（如 `write-yaochangyu-style`）時顯示。
- **自訂 ANSI 配色**：與 premium 暗色/灰色主題一致的精緻終端機配色。

## 系統需求與前置作業

- **Python 3**：地位列渲染腳本需要 Python 3。您可以執行 `python3 --version` 來檢查系統是否已安裝。
  - Ubuntu/Debian：`sudo apt update && sudo apt install -y python3`
  - macOS：`brew install python`
  - Windows (WSL)：`sudo apt install python3`

## 安裝步驟

### 1. 遠端一鍵安裝（推薦）

您無須 clone 本儲存庫，可以直接透過 `curl` 或 `wget` 執行 GitHub 上的安裝腳本，它會自動下載最新版的 `statusline.py`：

```bash
curl -sSL https://raw.githubusercontent.com/yaochangyu/antigravity-statusline/main/install.sh | bash
```

### 2. 本地開發安裝（適用於開發者）

如果您預計會自行客製化地位列腳本，請 clone 本儲存庫並執行本地安裝（會直接將腳本複製到您的設定目錄中）：

```bash
git clone https://github.com/yaochangyu/antigravity-statusline.git
cd antigravity-statusline
chmod +x install.sh
./install.sh
```

## 運作原理與配置

預設情況下，`antigravity-cli` 會讀取 `~/.gemini/antigravity-cli/settings.json` 的設定檔。若要套用自訂的 statusline，必須在設定檔中的 `"statusLine"` 區塊配置執行路徑。

本專案的 `install.sh` 安裝腳本會**自動為您修改此配置**。若您希望手動設定，請在您的 `settings.json` 中加入以下屬性。您也可以透過在 `"statusLine"` 區塊中添加 `"autoUpdate": true` 來啟用自動更新功能（這會在偵測到新版本時自動下載並覆蓋實體檔案，同時也會保護開發者的軟連結不受影響）：

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.gemini/antigravity-cli/scratch/statusline.py",
    "enabled": true,
    "autoUpdate": true
  }
}
```

## 更新腳本

本地位列腳本具備背景非阻塞式的自動檢查機制，每 24 小時會自動在背景偵測 GitHub 上是否有新版本。如果有可用更新，將在您的地位列 session 時間旁亮起 `(🌟Update Available)` 提示徽章。

### 1. 遠端一鍵更新
您可以直接從 GitHub 執行更新腳本：

```bash
curl -sSL https://raw.githubusercontent.com/yaochangyu/antigravity-statusline/main/update.sh | bash
```

### 2. 本地更新
如果您已將本儲存庫 clone 到本地，可以執行以下指令更新：

```bash
./update.sh
```

## 解除安裝

### 1. 遠端一鍵解除安裝
您可以直接從 GitHub 執行移除腳本：

```bash
curl -sSL https://raw.githubusercontent.com/yaochangyu/antigravity-statusline/main/uninstall.sh | bash
```

### 2. 本地解除安裝
如果您已將本儲存庫 clone 到本地，可以執行以下指令移除：

```bash
./uninstall.sh
```
