# Minic - 臺北醫學大學神經學研究資料庫平台
## 專案摘要報告

**報告日期**: 2025年11月4日
**專案名稱**: Minic (TMU Neurology Research Database Platform)
**GitHub 位置**: https://github.com/arbiterski/minic

---

## 📊 專案概述

Minic 是一個專為收集與整合神經科學及神經外科相關的臨床與研究資料而設計的開放式平台。本平台由臺北醫學大學經營，整合北醫附醫、萬芳醫院、雙和醫院三家附設醫院的臨床案例、研究數據與醫療資訊。

### 核心特色

- **資料去識別化處理**: 所有資料經嚴格去識別化與主題分類
- **跨機構整合**: 支持院內外研究人員進行跨領域與跨機構合作
- **開放協作模式**: 參考 PhysioNet 設計，促進數據可再利用
- **雙語支援**: 完整的繁體中文/英文雙語介面 **(最新功能)**

---

## 🚀 最新更新 (2025-11-04)

### ✨ 新功能：雙語支援系統

**Commit**: `f6838c20` - "Add bilingual support (Traditional Chinese / English)"

#### 實作內容：

1. **翻譯資料庫 (translations.js)**
   - 完整的中英文翻譯字典
   - 涵蓋所有 UI 元素（導航、篩選、按鈕、表單）
   - 280+ 翻譯鍵值對

2. **語言切換器**
   - Navbar 右上角地球圖示下拉選單
   - 🇹🇼 繁體中文 / 🇺🇸 English 選項
   - 即時切換，無需重新載入頁面

3. **語言管理系統**
   - LanguageManager class 管理語言狀態
   - localStorage 儲存用戶語言偏好
   - 自動套用上次選擇的語言

4. **HTML 更新**
   - 關鍵 UI 元素加入 `data-i18n` 屬性
   - 支援動態翻譯更新
   - 維持原有功能完整性

---

## 🗂️ 專案結構

```
dementiaDB/
├── app/                       # Flask 應用程式
├── templates/                 # HTML 模板
│   ├── index.html            # 首頁 (含雙語功能)
│   ├── about.html            # 關於頁面
│   └── database_detail.html  # 資料庫詳情頁
├── static/                    # 靜態資源
│   ├── css/style.css         # 樣式表
│   └── js/
│       ├── app.js            # 主要應用邏輯
│       └── translations.js    # 雙語翻譯系統 ⭐
├── data/                      # 資料檔案
├── scripts/                   # 工具腳本
├── tests/                     # 測試檔案
├── docker/                    # Docker 部署檔案
├── web_server.py             # 主要 Web 伺服器
├── requirements.txt          # Python 依賴套件
├── README.md                 # 專案說明
└── PROJECT_SUMMARY.md        # 專案摘要 (本文件)
```

---

## 📚 資料庫內容

### 1. 臺灣失智症臨床資料庫

**狀態**: ✅ 開放存取
**資料來源**: 臺北醫學大學雙和醫院失智症中心與神經內科

#### 資料規格
- **評估標準**: 美國國家老化研究院-阿茲海默症協會(NIA-AA)
- **資料期間**: 2012-2024
- **資料內容**:
  - 病歷與人口統計
  - 神經心理評估（MMSE、CASI、CDR）
  - 持續多年的追蹤數據
  - 腦部 MRI 影像（部分患者）
  - 腦萎縮與白質病灶評分

#### 研究應用
- 阿茲海默症異質性研究
- 疾病進展模式分析
- 個體化治療標的開發
- 機器學習亞型分群分析
- 跨中心橫斷及縱貫研究協作

#### 相關論文
📄 **Nguyen TTT, Lee HH, Huang LK, et al.**
*"Heterogeneity of Alzheimer's disease identified by neuropsychological test profiling"*
PLoS One. 2023;18(10):e0292527.
🔗 https://pubmed.ncbi.nlm.nih.gov/37797059/

### 2. 大腦意識資料庫

**狀態**: ⏳ 規劃中（限制存取）
**資料來源**: 臺北醫學大學腦科學研究中心

研究大腦意識狀態、認知功能和神經可塑性的綜合資料庫，包含：
- 腦電圖 (EEG)
- 功能性磁振造影 (fMRI)
- 多模態神經生理資料

---

## 💻 技術架構

### 後端技術
- **框架**: Flask (Python 3.9+)
- **資料處理**: Pandas, NumPy, Matplotlib
- **資料庫**: CSV 檔案格式（去識別化）

### 前端技術
- **框架**: Bootstrap 5
- **語言**: HTML5, CSS3, JavaScript (ES6+)
- **圖示庫**: Font Awesome 6.0
- **特色功能**:
  - 響應式設計
  - 即時搜尋與篩選
  - 雙語切換系統 ⭐

### 部署方式
- Docker 容器化支援
- 本地開發：`python web_server.py`
- 正式環境：Docker Compose

---

## 📦 安裝與執行

### 環境需求
```bash
Python 3.9+
pip
```

### 快速啟動

1. **克隆專案**
```bash
git clone https://github.com/arbiterski/minic.git
cd minic
```

2. **安裝依賴**
```bash
pip install -r requirements.txt
```

3. **執行應用程式**
```bash
python web_server.py
```

4. **開啟瀏覽器**
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

---

## 🔗 相關連結

- **專案網站**: https://neurologytmu.loinc100.org
- **GitHub**: https://github.com/arbiterski/minic
- **參考平台**: https://physionet.org/

---

## 📧 聯絡資訊

**平台管理**: neurology@tmu.edu.tw
**電話**: +886-2-2736-1661
**地址**: 臺北市信義區吳興街250號

---

## 📝 版本歷程

### v1.1.0 (2025-11-04) ⭐ 最新版本
- ✨ 新增雙語支援系統（繁體中文/英文）
- 🌐 實作語言切換功能與 LocalStorage 記憶
- 📄 建立完整翻譯資料庫
- 🔧 更新所有 UI 元素支援動態翻譯

### v1.0.3 (2025-09-03)
- 📝 更新倫理條款（新增受試者可隨時退出說明）

### v1.0.2 (2025-09-01)
- 🔗 更新專案網站 URL
- 📅 更新資料期間（2012-2020 → 2012-2024）

### v1.0.1 (2025-09-01)
- 📦 添加去識別化資料檔案 (anonymized_csv.zip)

### v1.0.0 (2025-08-27)
- 🎉 初始版本發布
- 🏥 建立失智症臨床資料庫平台
- 📊 PhysioNet 風格設計

---

## 📄 授權

本專案採用 **Creative Commons Attribution 4.0 International License** 授權。

---

## 🙏 致謝

本平台設計參考 [PhysioNet](https://physionet.org/) 的開放協作、數據可再利用模式，
感謝所有參與資料收集與研究的醫療團隊與研究人員。

---

**© 2025 臺北醫學大學 神經學研究資料庫平台 | 品牌為 Minic**
