# Alzheimer's Disease Analysis Database MVP

一個安全的阿茲海默症公開分析資料庫平台，支援 AI 生成的 Python 程式碼在隔離沙盒中執行。

## 專案概述

本專案實現了一個完整的資料分析流程：
1. **前端問題** → 2. **Claude 產生 Python 程式碼** → 3. **沙盒執行** → 4. **產生結果** → 5. **Web API 回傳**

## 架構特色

- **後端**: Python 3.11 + FastAPI + Uvicorn
- **任務佇列**: Redis + RQ 支援非同步執行
- **沙盒執行**: 獨立 Docker 映像，無網路存取
- **隱私保護**: k-匿名 (k=10) + 資料聚合
- **審計追蹤**: 完整的操作記錄和雜湊驗證

## 快速開始

### 前置需求

- Docker 和 Docker Compose
- Python 3.11+
- Redis

### 安裝步驟

1. **克隆專案**
```bash
git clone <repository-url>
cd dementiaDB
```

2. **建立環境變數檔案**
```bash
cp env.sample .env
# 編輯 .env 檔案，設定必要的配置
```

3. **建立沙盒映像**
```bash
cd docker
docker build -f sandbox.Dockerfile -t dementia-sandbox:latest .
cd ..
```

4. **啟動服務**
```bash
docker-compose up -d
```

5. **驗證安裝**
```bash
curl http://localhost:8000/health
```

## API 端點

### 主要端點

- `POST /api/v1/ask` - 提交分析問題
- `GET /api/v1/result/{job_id}` - 查詢工作狀態
- `GET /api/v1/files/{job_id}/{filename}` - 下載生成檔案
- `DELETE /api/v1/jobs/{job_id}` - 刪除工作

### 使用範例

```bash
# 提交分析問題
curl -X POST "http://localhost:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "分析患者年齡分佈",
    "outputs": ["plot", "table"],
    "privacy_level": "k_anonymous"
  }'

# 查詢結果
curl "http://localhost:8000/api/v1/result/{job_id}"
```

## 專案結構

```
dementiaDB/
├── app/                    # 主要應用程式
│   ├── api/               # API 端點
│   ├── core/              # 核心配置
│   ├── models/            # 資料模型
│   ├── services/          # 業務邏輯服務
│   └── utils/             # 工具函數
├── docker/                 # Docker 配置
│   ├── sandbox.Dockerfile # 沙盒映像
│   └── sandbox_runner.py  # 沙盒執行器
├── tests/                  # 測試檔案
├── docker-compose.yml      # 服務編排
├── Dockerfile             # 主應用映像
├── requirements.txt        # Python 依賴
└── README.md              # 專案說明
```

## 配置說明

### 環境變數

- `ANTHROPIC_API_KEY`: Claude API 金鑰
- `DATASET_PATH`: 資料集路徑
- `ARTIFACT_DIR`: 輸出檔案目錄
- `K_ANONYMITY`: k-匿名參數
- `REDIS_URL`: Redis 連線字串

### 資料集格式

支援兩種格式：
- **Parquet** (優先): `patients.parquet`
- **Excel**: `patients.xlsx`

## 隱私保護

### 隱私等級

1. **public**: 原始資料
2. **aggregated**: 資料聚合
3. **k_anonymous**: k-匿名保護 (預設 k=10)

### 安全措施

- 沙盒容器無網路存取
- 程式碼執行時間限制
- 記憶體和 CPU 使用限制
- 完整的審計日誌

## 開發指南

### 本地開發

```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動 Redis
docker run -d -p 6379:6379 redis:7-alpine

# 啟動應用
python -m app.main
```

### 執行測試

```bash
pytest
```

### 程式碼品質

- 使用型別註解
- 遵循 PEP 8 規範
- 完整的文件字串
- 單元測試覆蓋

## 部署

### 生產環境

1. 設定適當的環境變數
2. 配置反向代理 (Nginx)
3. 啟用 HTTPS
4. 設定監控和日誌
5. 配置備份策略

### Docker 部署

```bash
# 建立生產映像
docker build -t dementia-db:prod .

# 啟動服務
docker-compose -f docker-compose.prod.yml up -d
```

## 故障排除

### 常見問題

1. **沙盒容器啟動失敗**
   - 檢查 Docker 權限
   - 確認映像存在

2. **Redis 連線錯誤**
   - 檢查 Redis 服務狀態
   - 確認連線字串

3. **檔案權限問題**
   - 檢查目錄權限
   - 確認 Docker 卷掛載

## 貢獻指南

1. Fork 專案
2. 建立功能分支
3. 提交變更
4. 發起 Pull Request

## 授權

本專案採用 MIT 授權條款。

## 聯絡資訊

如有問題或建議，請開啟 Issue 或聯絡專案維護者。
