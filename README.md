# Pokémon Center Online 監控器

監控 https://www.pokemoncenter-online.com 網站狀態，當網站從維修狀態恢復正常時發送通知。

## 功能特色

- 🔍 監控網站可用性
- 🛠️ 自動檢測維修頁面
- 📧 Email 通知
- 💾 狀態記憶（避免重複通知）

## 使用方法

### 1. 安裝依賴

```bash
pip install requests python-dotenv
```

### 2. 設定配置

**本地測試時：**
複製 `config_example.env` 為 `.env`：

```bash
cp config_example.env .env
```

然後編輯 `.env` 檔案：


**Email 設定（可選）：**
- Gmail 用戶需要使用「應用程式密碼」，不是一般登入密碼
- 其他 email 服務商請修改 SMTP 設定

### 3. 執行監控

```bash
python3 pco_monitor.py
```

### 4. 雲端執行（推薦）

**GitHub Actions 自動執行：**
1. 推送程式碼到 GitHub repository
2. 在 GitHub repository 設定 → Secrets and variables → Actions 中新增：
   - Email 相關設定：`SMTP_HOST`, `SMTP_USER`, `SMTP_PASS`, `EMAIL_TO` 等
3. GitHub Actions 會每 5 分鐘自動執行監控

**本地定期執行：**
使用 cron 定期檢查（例如每 5 分鐘）：

```bash
# 編輯 crontab
crontab -e

# 加入以下行（每 5 分鐘檢查一次）
*/5 * * * * cd /path/to/your/script && /usr/bin/python3 pco_monitor.py
```

## 工作原理

1. 訪問 Pokémon Center Online 網站
2. 檢查 HTTP 狀態碼和頁面內容
3. 尋找維修相關關鍵字（「maintenance」、「メンテナンス」等）
4. 與上次檢查結果比較
5. 如果狀態從「DOWN」變為「UP」，發送通知

## 狀態檔案

腳本會建立 `pco_state.txt` 檔案來記錄上次的狀態，確保只在狀態改變時發送通知。 
