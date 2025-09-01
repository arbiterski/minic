# 臺灣失智症臨床資料庫 FHIR 格式

## 概述

本資料集包含臺灣失智症患者的臨床數據，以 FHIR (Fast Healthcare Interoperability Resources) 標準格式提供。資料來源為多個 CSV 檔案，經過去識別化處理後轉換為 FHIR 資源。

## FHIR 資源類型

本資料庫包含以下 FHIR 資源類型：

1. **Patient** - 患者基本資訊
2. **Observation** - 觀察結果，包括認知測試分數、生理指標等
3. **Condition** - 失智症診斷及相關病況
4. **Encounter** - 就診記錄
5. **MedicationRequest** - 藥物處方
6. **DiagnosticReport** - 診斷報告

## 資料來源

原始資料來自以下檔案：
- 107.csv
- 108.csv
- 109.csv
- 111.csv
- 112.csv
- 113.csv
- patients.xlsx

## 隱私保護

所有資料均經過去識別化處理，包括：
- 個人識別資訊（姓名、身分證字號、病歷號）已移除或雜湊處理
- 年齡已轉換為年齡段
- 應用 k-匿名保護 (k=10)

## 使用方式

您可以使用標準的 FHIR API 查詢工具來存取這些資源，例如：
- [HAPI FHIR](https://hapifhir.io/)
- [IBM FHIR Server](https://github.com/IBM/FHIR)
- [Pathling](https://pathling.csiro.au/)

## 引用

如使用本資料集，請引用：

```
臺北醫學大學. (2025). 臺灣失智症臨床資料庫 FHIR 格式 (版本 1.0.0).
```

## 版本資訊

- **版本**: 1.0.0
- **發布日期**: 2025年8月28日
- **最後更新**: 2025年8月28日

## 參考資料

本資料集的 FHIR 轉換參考了 MIMIC-IV Clinical Database Demo on FHIR：

Bennett, A., Ulrich, H., Wiedekopf, J., Szul, P., Grimes, J., & Johnson, A. (2025). MIMIC-IV Clinical Database Demo on FHIR (version 2.1.0). PhysioNet.

