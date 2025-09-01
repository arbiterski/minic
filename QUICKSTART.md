# 🚀 快速啟動指南

## 5分鐘快速啟動

### 1. 檢查環境
```bash
# 檢查專案狀態
./scripts/check_status.sh
```

### 2. 一鍵啟動（推薦）
```bash
# 完整設置和啟動
make full-start
```

### 3. 手動啟動（分步驟）
```bash
# 安裝依賴
make install

# 建立沙盒映像
make build-sandbox

# 建立範例資料
make sample-data

# 啟動服務
make start
```

### 4. 驗證安裝
```bash
# 檢查服務狀態
make status

# 測試 API
curl http://localhost:8000/health

# 查看 API 文檔
open http://localhost:8000/docs
```

## 🎯 常用命令

| 命令 | 說明 |
|------|------|
| `make help` | 顯示所有可用命令 |
| `make start` | 啟動開發環境 |
| `make stop` | 停止所有服務 |
| `make logs` | 查看服務日誌 |
| `make test` | 執行測試 |
| `make clean` | 清理環境 |
| `make status` | 檢查服務狀態 |

## 🌐 API 端點

- **健康檢查**: `GET /health`
- **API 文檔**: `GET /docs`
- **提交問題**: `POST /api/v1/ask`
- **查詢結果**: `GET /api/v1/result/{job_id}`
- **下載檔案**: `GET /api/v1/files/{job_id}/{filename}`

## 📊 測試 API

```bash
# 提交分析問題
curl -X POST "http://localhost:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "分析患者年齡分佈",
    "outputs": ["plot", "table"],
    "privacy_level": "k_anonymous"
  }'

# 查詢工作狀態
curl "http://localhost:8000/api/v1/result/{job_id}"
```

## 🔧 故障排除

### 常見問題

1. **Docker 未啟動**
   ```bash
   # 啟動 Docker Desktop
   open -a Docker
   ```

2. **端口被佔用**
   ```bash
   # 檢查端口使用
   lsof -i :8000
   
   # 停止服務
   make stop
   ```

3. **沙盒映像缺失**
   ```bash
   # 重新建立沙盒映像
   make build-sandbox
   ```

4. **依賴安裝失敗**
   ```bash
   # 清理並重新安裝
   pip uninstall -r requirements.txt
   make install
   ```

### 日誌查看

```bash
# 查看所有服務日誌
make logs

# 查看特定服務日誌
docker-compose logs -f web
docker-compose logs -f worker
docker-compose logs -f redis
```

## 📁 專案結構

```
dementiaDB/
├── app/                    # 主要應用程式
│   ├── api/               # API 端點
│   ├── core/              # 核心配置
│   ├── models/            # 資料模型
│   ├── services/          # 業務邏輯
│   └── utils/             # 工具函數
├── docker/                 # Docker 配置
├── scripts/                # 腳本工具
├── tests/                  # 測試檔案
├── data/                   # 資料集
├── artifacts/              # 輸出檔案
└── docker-compose.yml      # 服務編排
```

## 🎉 成功啟動後

1. **API 文檔**: http://localhost:8000/docs
2. **健康檢查**: http://localhost:8000/health
3. **服務狀態**: `make status`
4. **開始使用**: 提交第一個分析問題！

## 📞 需要幫助？

- 查看完整文檔: [README.md](README.md)
- 執行專案測試: `./scripts/test_project.py`
- 檢查專案狀態: `./scripts/check_status.sh`
- 查看 Makefile 幫助: `make help`
