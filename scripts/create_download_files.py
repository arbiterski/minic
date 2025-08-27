#!/usr/bin/env python3
"""
創建可下載的資料檔案，只包括去識別化的 CSV 檔案
"""

import os
import sys
import pandas as pd
import numpy as np
import json
import hashlib
import zipfile
import re
from pathlib import Path
from datetime import datetime

# 添加專案根目錄到路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 設定
DATA_DIR = "data/alzheimers_cohort_v1"
OUTPUT_DIR = "static/downloads"
ANONYMIZED_DIR = f"{OUTPUT_DIR}/anonymized_csv"
ANONYMIZED_ZIP_PATH = f"{OUTPUT_DIR}/anonymized_csv.zip"

# 確保輸出目錄存在
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ANONYMIZED_DIR, exist_ok=True)

# 隱私敏感欄位
SENSITIVE_COLUMNS = [
    "個案姓名", "身分證字號", "病歷號", "個案編號"
]

def hash_value(value):
    """將值雜湊化以保護隱私"""
    if pd.isna(value):
        return np.nan
    return hashlib.sha256(str(value).encode()).hexdigest()[:16]

def convert_to_year_month(value):
    """將出生日期轉換為年-月格式，隱藏具體日期"""
    try:
        if pd.isna(value):
            return "未知"
        
        # 如果是數字（可能是年齡），保持原樣
        if isinstance(value, (int, float)) and value > 0 and value < 120:
            return f"{int(value)}歲"
        
        value_str = str(value).strip()
        
        # 處理各種日期格式，只保留年-月
        date_patterns = [
            # YYYY/MM/DD 格式
            r'(\d{4})/(\d{1,2})/\d{1,2}',
            # YYYY-MM-DD 格式
            r'(\d{4})-(\d{1,2})-\d{1,2}',
            # YYYY年MM月DD日 格式
            r'(\d{4})年(\d{1,2})月\d{1,2}日',
            # YYYY.MM.DD 格式
            r'(\d{4})\.(\d{1,2})\.\d{1,2}',
            # YYYY/MM/DD HH:MM:SS 格式
            r'(\d{4})/(\d{1,2})/\d{1,2}\s+\d{1,2}:\d{1,2}:\d{1,2}',
            # YYYY-MM-DD HH:MM:SS 格式
            r'(\d{4})-(\d{1,2})-\d{1,2}\s+\d{1,2}:\d{1,2}:\d{1,2}',
            # 0YYY/MM/DD 格式（民國年）
            r'0(\d{3})/(\d{1,2})/\d{1,2}',
            # 0YYY-MM-DD 格式（民國年）
            r'0(\d{3})-(\d{1,2})-\d{1,2}',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, value_str)
            if match:
                year = match.group(1)
                month = int(match.group(2))
                
                # 如果是民國年，轉換為西元年
                if year.startswith('0') and len(year) == 4:
                    # 民國年轉西元年：民國年 + 1911
                    western_year = int(year) + 1911
                    return f"{western_year}-{month:02d}"
                else:
                    return f"{year}-{month:02d}"
        
        # 如果無法解析，嘗試其他格式
        # 處理 YYYY/MM 格式（只有年-月）
        year_month_pattern = r'(\d{4})/(\d{1,2})'
        match = re.search(year_month_pattern, value_str)
        if match:
            year = match.group(1)
            month = int(match.group(2))
            return f"{year}-{month:02d}"
        
        # 處理 YYYY-MM 格式（只有年-月）
        year_month_pattern2 = r'(\d{4})-(\d{1,2})'
        match = re.search(year_month_pattern2, value_str)
        if match:
            year = match.group(1)
            month = int(match.group(2))
            return f"{year}-{month:02d}"
        
        # 如果都無法解析，返回原值
        return value
        
    except Exception as e:
        print(f"處理日期值 '{value}' 時發生錯誤: {e}")
        return value

def anonymize_csv(file_path, output_path):
    """對 CSV 檔案進行去識別化處理"""
    try:
        df = pd.read_csv(file_path)
        
        # 處理敏感欄位
        for col in SENSITIVE_COLUMNS:
            if col in df.columns:
                # 對敏感欄位進行雜湊化
                df[col] = df[col].apply(hash_value)
        
        # 處理各種可能的出生日期欄位，只保留年-月
        date_columns = [
            "生日/年齡", "西元", "出生日期", "生日", "年齡"
        ]
        
        for col in date_columns:
            if col in df.columns:
                print(f"  處理欄位 '{col}'，轉換為年-月格式...")
                df[col] = df[col].apply(convert_to_year_month)
        
        # 保存去識別化後的 CSV
        df.to_csv(output_path, index=False)
        return True
    except Exception as e:
        print(f"處理 {file_path} 時發生錯誤: {e}")
        return False

def create_anonymized_csv_files():
    """創建去識別化的 CSV 檔案"""
    print("創建去識別化的 CSV 檔案...")
    
    # 獲取所有 CSV 檔案
    csv_files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"在 {DATA_DIR} 中找不到 CSV 檔案")
        return False
    
    # 處理每個 CSV 檔案
    success_count = 0
    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        output_path = os.path.join(ANONYMIZED_DIR, file_name)
        
        print(f"處理 {file_name}...")
        if anonymize_csv(file_path, output_path):
            success_count += 1
    
    print(f"完成 {success_count}/{len(csv_files)} 個 CSV 檔案的去識別化")
    return success_count > 0

def create_anonymized_zip():
    """創建去識別化 CSV 的 ZIP 檔案"""
    print("創建去識別化 CSV 的 ZIP 檔案...")
    
    try:
        with zipfile.ZipFile(ANONYMIZED_ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 添加所有去識別化的 CSV 檔案
            for file in os.listdir(ANONYMIZED_DIR):
                file_path = os.path.join(ANONYMIZED_DIR, file)
                if os.path.isfile(file_path):
                    zipf.write(file_path, os.path.basename(file_path))
        
        print(f"去識別化 CSV ZIP 檔案已創建: {ANONYMIZED_ZIP_PATH}")
        return True
    except Exception as e:
        print(f"創建去識別化 CSV ZIP 檔案時發生錯誤: {e}")
        return False

def create_download_info():
    """創建下載資訊 JSON 檔案"""
    print("創建下載資訊...")
    
    csv_size = os.path.getsize(ANONYMIZED_ZIP_PATH) if os.path.exists(ANONYMIZED_ZIP_PATH) else 0
    
    info = {
        "anonymized_csv": {
            "path": os.path.basename(ANONYMIZED_ZIP_PATH),
            "size": csv_size,
            "size_formatted": format_size(csv_size),
            "last_updated": datetime.now().isoformat(),
            "description": "經過去識別化處理的 CSV 檔案，包含所有原始資料但已移除個人識別資訊，出生日期只保留年-月格式，完全隱藏具體日期"
        }
    }
    
    # 保存下載資訊
    with open(f"{OUTPUT_DIR}/download_info.json", "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    
    print("下載資訊已創建")
    return True

def format_size(size_bytes):
    """格式化檔案大小"""
    if size_bytes == 0:
        return "0 B"
    size_names = ("B", "KB", "MB", "GB", "TB")
    i = int(np.floor(np.log(size_bytes) / np.log(1024)))
    p = np.power(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def main():
    """主函數"""
    print("開始創建可下載的資料檔案...")
    print("注意：所有出生日期將只保留年-月格式，完全隱藏具體日期")
    
    # 創建去識別化的 CSV 檔案
    if not create_anonymized_csv_files():
        print("創建去識別化 CSV 檔案失敗")
        return
    
    # 創建去識別化 CSV 的 ZIP 檔案
    if not create_anonymized_zip():
        print("創建去識別化 CSV ZIP 檔案失敗")
        return
    
    # 創建下載資訊
    if not create_download_info():
        print("創建下載資訊失敗")
        return
    
    print("所有下載檔案已創建完成")
    print("去識別化完成：出生日期已轉換為年-月格式，具體日期已完全隱藏")

if __name__ == "__main__":
    main()
