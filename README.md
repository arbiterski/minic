# Minic - 臺北醫學大學神經學研究資料庫平台

## 專案簡介

Minic 是一個專為收集與整合神經科學及神經外科相關的臨床與研究資料而設計的平台。本網站由臺北醫學大學經營，資料平台涵蓋神經內科與神經外科領域，彙集自台北醫學大學體系內三家附設醫院（北醫附醫、萬芳醫院、雙和醫院）之臨床案例、研究數據、影像檔案及多面向醫療資訊。

## 主要功能

- **資料庫管理**：整合多個神經學研究資料庫
- **資料去識別化**：所有資料經嚴格去識別化與主題分類
- **研究合作**：促進神經醫學研究、教學與臨床之資源共享
- **跨機構合作**：支持院內外研究人員進行跨領域與跨機構合作

## 技術架構

- **後端**：Flask (Python)
- **前端**：HTML5, CSS3, JavaScript, Bootstrap 5
- **資料處理**：Pandas, NumPy, Matplotlib
- **資料庫**：CSV 檔案格式
- **部署**：Docker 支援

## 專案結構

```
dementiaDB/
├── app/                    # 主要應用程式
├── templates/             # HTML 模板
├── static/                # 靜態檔案 (CSS, JS, 圖片)
├── data/                  # 資料檔案
├── scripts/               # 腳本檔案
├── tests/                 # 測試檔案
├── docker/                # Docker 相關檔案
├── web_server.py          # 主要 Web 服務器
├── requirements.txt       # Python 依賴套件
└── README.md             # 專案說明文件
```

## 安裝與執行

### 環境需求

- Python 3.9+
- pip

### 安裝步驟

1. 克隆專案
```bash
git clone https://github.com/yourusername/minic.git
cd minic
```

2. 安裝依賴套件
```bash
pip install -r requirements.txt
```

3. 執行應用程式
```bash
python web_server.py
```

4. 開啟瀏覽器訪問
```
http://localhost:5001
```

### Docker 部署

```bash
# 建構映像檔
docker build -t minic .

# 執行容器
docker run -p 5001:5001 minic
```

## 資料庫內容

### 臺灣失智症臨床資料庫

- **資料來源**：臺北醫學大學雙和醫院失智症中心與神經內科
- **評估標準**：美國國家老化研究院-阿茲海默症協會(NIA-AA)
- **資料內容**：病歷、神經心理評估（MMSE、CASI、CDR）、腦部MRI影像
- **特色**：機器學習方法進行異質性分類，促進亞型分群分析

### 大腦意識資料庫

- **研究領域**：大腦意識狀態、認知功能和神經可塑性
- **資料類型**：腦電圖、功能性磁振造影等多模態資料
- **狀態**：規劃中

## 研究領域

### 神經內科
- 阿茲海默症與失智症
- 帕金森氏症
- 腦中風
- 癲癇
- 多發性硬化症

### 神經外科
- 腦腫瘤
- 腦血管疾病
- 脊椎疾病
- 創傷性腦損傷
- 功能性神經外科

## 聯絡資訊

- **平台管理**：neurology@tmu.edu.tw
- **電話**：+886-2-2736-1661
- **地址**：臺北市信義區吳興街250號

## 授權

本專案採用 Creative Commons Attribution 4.0 International License 授權。

## 貢獻

我們歡迎研究人員提交新的資料庫，共同推進神經科學研究發展。

## 參考

本平台設計參考 [PhysioNet](https://physionet.org/) 的開放協作、數據可再利用模式。

---

© 2025 臺北醫學大學 神經學研究資料庫平台 | 品牌為 Minic

