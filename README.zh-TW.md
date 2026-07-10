# Antigravity Statusline (繁體中文)

[English](README.md) | [繁體中文](README.zh-TW.md)

這是一個適用於 `antigravity-cli`（及 Claude Code 環境）的自訂 Python 地位列 (Statusline) 腳本。它能即時顯示 Git 分支資訊、API 額度限制、當前累積花費、Session 持續時間以及執行中的 Agent 技能。

## 功能特色

- **Git 狀態**：顯示當前分支、變動狀態 (`*`)，以及領先/落後 (ahead/behind) 的 commit 數量。
- **額度限制**：以自訂進度條顯示 5 小時及每週的 API 額度使用量與重置倒數。
- **費用監控**：直接顯示今日與本月的 API 累計花費金額（不使用無謂的每日限制）。
- **真實技能偵測**：動態解析對話紀錄 (Transcript)，僅在載入真實技能（如 `write-yaochangyu-style`）時顯示。
- **自訂 ANSI 配色**：與 premium 暗色/灰色主題一致的精緻終端機配色。

## 安裝步驟

執行安裝腳本，將此專案目錄下的 `statusline.py` 軟連結 (symlink) 至作用中的 `.gemini` 設定目錄中：

```bash
chmod +x install.sh
./install.sh
```
