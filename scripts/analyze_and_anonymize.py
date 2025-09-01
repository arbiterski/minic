#!/usr/bin/env python3
"""
分析資料夾中的所有 CSV 檔案並進行去識別化處理
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import hashlib
import json
from datetime import datetime

# 添加專案根目錄到路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 導入隱私保護工具
from app.utils.privacy import apply_k_anonymity, aggregate_data, sanitize_outputs

# 設定
DATA_DIR = "data/alzheimers_cohort_v1"
OUTPUT_DIR = "artifacts/anonymized_data"
ANALYSIS_DIR = "artifacts/analysis_results"
K_ANONYMITY_VALUE = 10

# 確保輸出目錄存在
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)

# 隱私敏感欄位 (這些欄位將被特別處理)
SENSITIVE_COLUMNS = [
    "個案姓名", "身分證字號", "病歷號", "生日/年齡", "個案編號"
]

def hash_value(value):
    """將值雜湊化以保護隱私"""
    if pd.isna(value):
        return np.nan
    return hashlib.sha256(str(value).encode()).hexdigest()[:16]

def anonymize_dataframe(df, k=K_ANONYMITY_VALUE):
    """對資料進行去識別化處理"""
    # 複製資料框以避免修改原始資料
    anon_df = df.copy()
    
    # 1. 處理敏感欄位
    for col in SENSITIVE_COLUMNS:
        if col in anon_df.columns:
            if col == "生日/年齡":
                # 將年齡轉換為年齡段
                try:
                    anon_df[col] = pd.to_numeric(anon_df[col], errors='coerce')
                    anon_df[col] = pd.cut(anon_df[col], 
                                         bins=[0, 50, 60, 70, 80, 90, 120],
                                         labels=['<50歲', '50-59歲', '60-69歲', '70-79歲', '80-89歲', '90+歲'])
                except:
                    anon_df[col] = "未知年齡"
            else:
                # 其他敏感欄位進行雜湊化
                anon_df[col] = anon_df[col].apply(hash_value)
    
    # 2. 應用 k-匿名化
    anon_df = apply_k_anonymity(anon_df, k)
    
    return anon_df

def analyze_csv(file_path):
    """分析 CSV 檔案並產生統計資訊"""
    try:
        # 讀取 CSV 檔案
        df = pd.read_csv(file_path)
        file_name = os.path.basename(file_path)
        
        # 基本統計資訊
        stats = {
            "file_name": file_name,
            "record_count": len(df),
            "column_count": len(df.columns),
            "columns": list(df.columns),
            "memory_usage": df.memory_usage(deep=True).sum() / (1024 * 1024),  # MB
            "timestamp": datetime.now().isoformat()
        }
        
        # 創建輸出目錄
        file_base = os.path.splitext(file_name)[0]
        output_path = os.path.join(ANALYSIS_DIR, file_base)
        os.makedirs(output_path, exist_ok=True)
        
        # 保存統計資訊
        with open(os.path.join(output_path, "stats.json"), "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        # 去識別化處理
        anon_df = anonymize_dataframe(df)
        
        # 保存去識別化後的資料
        anon_output_path = os.path.join(OUTPUT_DIR, f"{file_base}_anonymized.csv")
        anon_df.to_csv(anon_output_path, index=False)
        
        # 產生視覺化圖表
        generate_visualizations(df, anon_df, output_path, file_base)
        
        return {
            "file_name": file_name,
            "original_path": file_path,
            "anonymized_path": anon_output_path,
            "analysis_path": output_path,
            "status": "success"
        }
        
    except Exception as e:
        print(f"處理 {file_path} 時發生錯誤: {e}")
        return {
            "file_name": os.path.basename(file_path),
            "status": "error",
            "error": str(e)
        }

def generate_visualizations(df, anon_df, output_path, file_base):
    """產生視覺化圖表"""
    try:
        # 設定中文字型
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Microsoft JhengHei', 'PingFang TC', 'Heiti TC']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 1. 性別分布圓餅圖
        if "性別" in df.columns:
            plt.figure(figsize=(10, 6))
            gender_counts = df["性別"].value_counts()
            plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90)
            plt.title(f'{file_base} - 性別分布')
            plt.tight_layout()
            plt.savefig(os.path.join(output_path, "gender_distribution.png"))
            plt.close()
        
        # 2. 年齡分布直方圖
        age_col = None
        for col in df.columns:
            if "年齡" in col or "生日" in col:
                age_col = col
                break
                
        if age_col:
            try:
                ages = pd.to_numeric(df[age_col], errors='coerce')
                ages = ages[(ages > 0) & (ages < 120)]  # 過濾有效年齡
                
                plt.figure(figsize=(10, 6))
                sns.histplot(ages, bins=20, kde=True)
                plt.title(f'{file_base} - 年齡分布')
                plt.xlabel('年齡')
                plt.ylabel('人數')
                plt.tight_layout()
                plt.savefig(os.path.join(output_path, "age_distribution.png"))
                plt.close()
                
                # 年齡統計表
                age_stats = ages.describe().to_frame('年齡統計')
                age_stats.to_csv(os.path.join(output_path, "age_stats.csv"))
            except:
                print(f"無法處理年齡欄位: {age_col}")
        
        # 3. 失智程度分布 (如果有此欄位)
        dementia_col = None
        for col in df.columns:
            if "失智" in col and "程度" in col:
                dementia_col = col
                break
                
        if dementia_col:
            plt.figure(figsize=(12, 6))
            dementia_counts = df[dementia_col].value_counts()
            sns.barplot(x=dementia_counts.index, y=dementia_counts.values)
            plt.title(f'{file_base} - 失智程度分布')
            plt.xlabel('失智程度')
            plt.ylabel('人數')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(output_path, "dementia_level_distribution.png"))
            plt.close()
            
        # 4. 相關性熱圖 (僅針對數值型資料)
        numeric_df = df.select_dtypes(include=[np.number])
        if not numeric_df.empty and numeric_df.shape[1] > 1:
            plt.figure(figsize=(12, 10))
            corr_matrix = numeric_df.corr()
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
            plt.title(f'{file_base} - 數值欄位相關性')
            plt.tight_layout()
            plt.savefig(os.path.join(output_path, "correlation_heatmap.png"))
            plt.close()
            
        # 5. 去識別化前後對比
        if age_col:
            try:
                # 原始年齡分布
                orig_ages = pd.to_numeric(df[age_col], errors='coerce')
                orig_ages = orig_ages[(orig_ages > 0) & (orig_ages < 120)]
                
                plt.figure(figsize=(12, 6))
                plt.subplot(1, 2, 1)
                sns.histplot(orig_ages, bins=20, kde=True)
                plt.title('原始年齡分布')
                plt.xlabel('年齡')
                plt.ylabel('人數')
                
                # 去識別化後年齡分布
                if age_col in anon_df.columns:
                    plt.subplot(1, 2, 2)
                    anon_df[age_col].value_counts().plot(kind='bar')
                    plt.title('去識別化後年齡分布')
                    plt.xlabel('年齡段')
                    plt.ylabel('人數')
                
                plt.tight_layout()
                plt.savefig(os.path.join(output_path, "age_comparison.png"))
                plt.close()
            except:
                print(f"無法生成年齡對比圖")
        
    except Exception as e:
        print(f"生成視覺化圖表時發生錯誤: {e}")

def generate_summary_report(results):
    """生成分析摘要報告"""
    summary = {
        "total_files": len(results),
        "success_count": sum(1 for r in results if r["status"] == "success"),
        "error_count": sum(1 for r in results if r["status"] == "error"),
        "total_records": sum(r.get("record_count", 0) for r in results if "record_count" in r),
        "timestamp": datetime.now().isoformat(),
        "files": results
    }
    
    # 保存摘要報告
    with open(os.path.join(ANALYSIS_DIR, "summary_report.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    # 生成 HTML 報告
    html_report = generate_html_report(summary)
    with open(os.path.join(ANALYSIS_DIR, "report.html"), "w", encoding="utf-8") as f:
        f.write(html_report)
    
    return summary

def generate_html_report(summary):
    """生成 HTML 格式的報告"""
    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>資料分析與去識別化報告</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; color: #333; }}
        h1, h2, h3 {{ color: #0056b3; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .summary {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .file-card {{ background-color: white; border-left: 4px solid #0056b3; padding: 15px; margin-bottom: 15px; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .file-card.error {{ border-left-color: #dc3545; }}
        .file-card h3 {{ margin-top: 0; }}
        .stats {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 10px; }}
        .stat-item {{ background-color: #e9ecef; padding: 5px 10px; border-radius: 4px; font-size: 14px; }}
        .images {{ display: flex; flex-wrap: wrap; gap: 15px; margin-top: 15px; }}
        .image-container {{ width: 300px; }}
        .image-container img {{ max-width: 100%; border: 1px solid #ddd; border-radius: 4px; }}
        .download-links {{ margin-top: 15px; }}
        .download-link {{ display: inline-block; background-color: #0056b3; color: white; padding: 8px 15px; text-decoration: none; border-radius: 4px; margin-right: 10px; }}
        .download-link:hover {{ background-color: #004494; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>資料分析與去識別化報告</h1>
        <div class="summary">
            <h2>摘要</h2>
            <p>總檔案數: {summary["total_files"]}</p>
            <p>成功處理: {summary["success_count"]}</p>
            <p>處理失敗: {summary["error_count"]}</p>
            <p>生成時間: {summary["timestamp"]}</p>
        </div>
        
        <h2>檔案詳情</h2>
"""
    
    # 添加每個檔案的詳情
    for file_result in summary["files"]:
        if file_result["status"] == "success":
            file_name = file_result["file_name"]
            file_base = os.path.splitext(file_name)[0]
            
            html += f"""
        <div class="file-card">
            <h3>{file_name}</h3>
            <div class="stats">
                <div class="stat-item">狀態: 成功</div>
            </div>
            <div class="download-links">
                <a href="../{file_result["anonymized_path"]}" class="download-link">下載去識別化資料</a>
                <a href="{file_base}/stats.json" class="download-link">查看統計資訊</a>
            </div>
            <div class="images">
                <div class="image-container">
                    <h4>年齡分布</h4>
                    <img src="{file_base}/age_distribution.png" alt="年齡分布" onerror="this.style.display='none'">
                </div>
                <div class="image-container">
                    <h4>性別分布</h4>
                    <img src="{file_base}/gender_distribution.png" alt="性別分布" onerror="this.style.display='none'">
                </div>
                <div class="image-container">
                    <h4>失智程度分布</h4>
                    <img src="{file_base}/dementia_level_distribution.png" alt="失智程度分布" onerror="this.style.display='none'">
                </div>
                <div class="image-container">
                    <h4>去識別化前後對比</h4>
                    <img src="{file_base}/age_comparison.png" alt="去識別化前後對比" onerror="this.style.display='none'">
                </div>
            </div>
        </div>
"""
        else:
            html += f"""
        <div class="file-card error">
            <h3>{file_result["file_name"]}</h3>
            <div class="stats">
                <div class="stat-item">狀態: 失敗</div>
            </div>
            <p>錯誤信息: {file_result.get("error", "未知錯誤")}</p>
        </div>
"""
    
    html += """
    </div>
</body>
</html>
"""
    return html

def main():
    """主函數"""
    print("開始分析與去識別化處理...")
    
    # 獲取所有 CSV 檔案
    csv_files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"在 {DATA_DIR} 中找不到 CSV 檔案")
        return
    
    print(f"找到 {len(csv_files)} 個 CSV 檔案")
    
    # 處理每個 CSV 檔案
    results = []
    for file_path in csv_files:
        print(f"處理 {file_path}...")
        result = analyze_csv(file_path)
        results.append(result)
        print(f"完成 {file_path} 處理，狀態: {result['status']}")
    
    # 生成摘要報告
    summary = generate_summary_report(results)
    
    print(f"分析與去識別化處理完成")
    print(f"成功處理: {summary['success_count']} 個檔案")
    print(f"處理失敗: {summary['error_count']} 個檔案")
    print(f"報告已保存至: {os.path.join(ANALYSIS_DIR, 'report.html')}")
    print(f"去識別化資料已保存至: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()

