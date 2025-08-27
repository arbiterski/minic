#!/usr/bin/env python3
"""
將 CSV 資料轉換為 FHIR 格式
"""

import os
import sys
import pandas as pd
import numpy as np
import json
import hashlib
import uuid
from pathlib import Path
from datetime import datetime, date
import re

# 添加專案根目錄到路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 設定
DATA_DIR = "data/alzheimers_cohort_v1"
OUTPUT_DIR = "fhir/resources"
K_ANONYMITY_VALUE = 10

# 確保輸出目錄存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

# FHIR 資源類型
RESOURCE_TYPES = {
    "Patient": os.path.join(OUTPUT_DIR, "Patient"),
    "Observation": os.path.join(OUTPUT_DIR, "Observation"),
    "Condition": os.path.join(OUTPUT_DIR, "Condition"),
    "Encounter": os.path.join(OUTPUT_DIR, "Encounter"),
    "MedicationRequest": os.path.join(OUTPUT_DIR, "MedicationRequest"),
    "DiagnosticReport": os.path.join(OUTPUT_DIR, "DiagnosticReport")
}

# 為每種資源類型創建目錄
for dir_path in RESOURCE_TYPES.values():
    os.makedirs(dir_path, exist_ok=True)

# 隱私敏感欄位
SENSITIVE_COLUMNS = [
    "個案姓名", "身分證字號", "病歷號", "生日/年齡", "個案編號"
]

def generate_uuid(value):
    """生成一致的 UUID，相同輸入產生相同 UUID"""
    if pd.isna(value):
        return str(uuid.uuid4())
    hash_obj = hashlib.md5(str(value).encode())
    return str(uuid.UUID(hash_obj.hexdigest()))

def hash_value(value):
    """將值雜湊化以保護隱私"""
    if pd.isna(value):
        return None
    return hashlib.sha256(str(value).encode()).hexdigest()[:16]

def convert_to_age_group(age_value):
    """將年齡轉換為年齡段"""
    try:
        age = float(age_value)
        if age < 50:
            return "<50歲"
        elif age < 60:
            return "50-59歲"
        elif age < 70:
            return "60-69歲"
        elif age < 80:
            return "70-79歲"
        elif age < 90:
            return "80-89歲"
        else:
            return "90+歲"
    except (ValueError, TypeError):
        return "未知年齡"

def create_patient_resource(patient_data):
    """創建 Patient 資源"""
    patient_id = generate_uuid(patient_data.get("個案編號", "") + patient_data.get("身分證字號", ""))
    
    # 處理性別
    gender = "unknown"
    if "性別" in patient_data:
        gender_value = patient_data["性別"]
        if gender_value == "男":
            gender = "male"
        elif gender_value == "女":
            gender = "female"
    
    # 處理年齡
    age_group = None
    if "生日/年齡" in patient_data:
        age_group = convert_to_age_group(patient_data["生日/年齡"])
    
    # 創建 Patient 資源
    patient_resource = {
        "resourceType": "Patient",
        "id": patient_id,
        "meta": {
            "profile": ["http://hl7.org/fhir/R4/patient.html"],
            "versionId": "1",
            "lastUpdated": datetime.now().isoformat()
        },
        "identifier": [
            {
                "system": "http://tmu.edu.tw/fhir/alzheimers/patient-id",
                "value": hash_value(patient_data.get("個案編號", ""))
            }
        ],
        "active": True,
        "gender": gender,
        "extension": []
    }
    
    # 添加年齡段擴展
    if age_group:
        patient_resource["extension"].append({
            "url": "http://tmu.edu.tw/fhir/alzheimers/age-group",
            "valueString": age_group
        })
    
    return patient_resource

def create_condition_resource(condition_data, patient_id):
    """創建 Condition 資源"""
    condition_id = generate_uuid(f"{patient_id}_{condition_data.get('失智症診斷', '')}")
    
    # 處理失智程度
    severity = None
    if "失智程度" in condition_data:
        severity = condition_data["失智程度"]
    
    # 創建 Condition 資源
    condition_resource = {
        "resourceType": "Condition",
        "id": condition_id,
        "meta": {
            "profile": ["http://hl7.org/fhir/R4/condition.html"],
            "versionId": "1",
            "lastUpdated": datetime.now().isoformat()
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "code": {
            "coding": [
                {
                    "system": "http://tmu.edu.tw/fhir/alzheimers/diagnosis",
                    "code": hash_value(condition_data.get("失智症診斷", "")),
                    "display": "失智症"
                }
            ],
            "text": "失智症"
        },
        "clinicalStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                    "code": "active",
                    "display": "Active"
                }
            ]
        },
        "verificationStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                    "code": "confirmed",
                    "display": "Confirmed"
                }
            ]
        }
    }
    
    # 添加嚴重程度
    if severity:
        condition_resource["severity"] = {
            "coding": [
                {
                    "system": "http://tmu.edu.tw/fhir/alzheimers/dementia-severity",
                    "code": hash_value(severity),
                    "display": severity
                }
            ],
            "text": severity
        }
    
    return condition_resource

def create_observation_resource(observation_data, patient_id):
    """創建 Observation 資源"""
    observation_id = generate_uuid(f"{patient_id}_{observation_data.get('觀察項目', '')}_{observation_data.get('觀察時間', '')}")
    
    # 創建 Observation 資源
    observation_resource = {
        "resourceType": "Observation",
        "id": observation_id,
        "meta": {
            "profile": ["http://hl7.org/fhir/R4/observation.html"],
            "versionId": "1",
            "lastUpdated": datetime.now().isoformat()
        },
        "status": "final",
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "code": {
            "coding": [
                {
                    "system": "http://tmu.edu.tw/fhir/alzheimers/observation",
                    "code": hash_value(observation_data.get("觀察項目", "")),
                    "display": observation_data.get("觀察項目", "未知觀察")
                }
            ],
            "text": observation_data.get("觀察項目", "未知觀察")
        }
    }
    
    # 添加觀察值
    if "觀察值" in observation_data:
        try:
            value = float(observation_data["觀察值"])
            observation_resource["valueQuantity"] = {
                "value": value,
                "unit": observation_data.get("單位", ""),
                "system": "http://unitsofmeasure.org",
                "code": observation_data.get("單位代碼", "")
            }
        except (ValueError, TypeError):
            observation_resource["valueString"] = str(observation_data["觀察值"])
    
    return observation_resource

def extract_observations_from_row(row, patient_id):
    """從資料行中提取觀察項目"""
    observations = []
    
    # 檢查可能的觀察項目欄位
    for col in row.index:
        # 跳過已知的非觀察項目欄位
        if col in SENSITIVE_COLUMNS or col == "性別" or "失智" in col:
            continue
        
        # 如果有值，創建觀察項目
        if pd.notna(row[col]) and row[col] != "":
            observation_data = {
                "觀察項目": col,
                "觀察值": row[col],
                "觀察時間": row.get("收案日期", datetime.now().isoformat())
            }
            observations.append(create_observation_resource(observation_data, patient_id))
    
    return observations

def process_csv_file(file_path):
    """處理 CSV 檔案並轉換為 FHIR 資源"""
    try:
        print(f"處理檔案: {file_path}")
        df = pd.read_csv(file_path)
        file_name = os.path.basename(file_path)
        
        patients = []
        conditions = []
        observations = []
        
        # 處理每一行資料
        for _, row in df.iterrows():
            # 創建 Patient 資源
            patient_resource = create_patient_resource(row)
            patient_id = patient_resource["id"]
            patients.append(patient_resource)
            
            # 如果有失智症診斷，創建 Condition 資源
            if "失智症診斷" in row and pd.notna(row["失智症診斷"]):
                condition_resource = create_condition_resource(row, patient_id)
                conditions.append(condition_resource)
            
            # 提取觀察項目
            patient_observations = extract_observations_from_row(row, patient_id)
            observations.extend(patient_observations)
        
        # 保存 FHIR 資源
        save_resources("Patient", patients)
        save_resources("Condition", conditions)
        save_resources("Observation", observations)
        
        print(f"完成處理檔案: {file_path}")
        print(f"創建了 {len(patients)} 個 Patient 資源")
        print(f"創建了 {len(conditions)} 個 Condition 資源")
        print(f"創建了 {len(observations)} 個 Observation 資源")
        
        return {
            "file_name": file_name,
            "patient_count": len(patients),
            "condition_count": len(conditions),
            "observation_count": len(observations),
            "status": "success"
        }
        
    except Exception as e:
        print(f"處理 {file_path} 時發生錯誤: {e}")
        return {
            "file_name": os.path.basename(file_path),
            "status": "error",
            "error": str(e)
        }

def save_resources(resource_type, resources):
    """保存 FHIR 資源到檔案"""
    output_dir = RESOURCE_TYPES[resource_type]
    
    for resource in resources:
        resource_id = resource["id"]
        output_path = os.path.join(output_dir, f"{resource_id}.json")
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(resource, f, ensure_ascii=False, indent=2)

def create_bundle(resource_type, resources):
    """創建 FHIR Bundle 資源"""
    bundle = {
        "resourceType": "Bundle",
        "id": f"{resource_type.lower()}-bundle-{datetime.now().strftime('%Y%m%d')}",
        "type": "collection",
        "entry": []
    }
    
    for resource in resources:
        bundle["entry"].append({
            "fullUrl": f"urn:uuid:{resource['id']}",
            "resource": resource
        })
    
    return bundle

def create_capability_statement():
    """創建 CapabilityStatement 資源"""
    capability = {
        "resourceType": "CapabilityStatement",
        "id": "tmu-alzheimers-fhir-server",
        "url": "http://tmu.edu.tw/fhir/alzheimers/metadata",
        "version": "1.0.0",
        "name": "TaiwanAlzheimersDatabase",
        "title": "臺灣失智症臨床資料庫 FHIR API",
        "status": "active",
        "date": datetime.now().isoformat(),
        "publisher": "臺北醫學大學",
        "description": "臺灣失智症臨床資料庫 FHIR 服務的能力聲明",
        "kind": "instance",
        "implementation": {
            "description": "臺灣失智症臨床資料庫 FHIR 服務",
            "url": "http://tmu.edu.tw/fhir/alzheimers"
        },
        "fhirVersion": "4.0.1",
        "format": [
            "json"
        ],
        "rest": [
            {
                "mode": "server",
                "resource": [
                    {
                        "type": "Patient",
                        "interaction": [
                            {
                                "code": "read"
                            },
                            {
                                "code": "search-type"
                            }
                        ],
                        "searchParam": [
                            {
                                "name": "gender",
                                "type": "token",
                                "documentation": "患者性別"
                            }
                        ]
                    },
                    {
                        "type": "Condition",
                        "interaction": [
                            {
                                "code": "read"
                            },
                            {
                                "code": "search-type"
                            }
                        ],
                        "searchParam": [
                            {
                                "name": "subject",
                                "type": "reference",
                                "documentation": "患者參考"
                            }
                        ]
                    },
                    {
                        "type": "Observation",
                        "interaction": [
                            {
                                "code": "read"
                            },
                            {
                                "code": "search-type"
                            }
                        ],
                        "searchParam": [
                            {
                                "name": "subject",
                                "type": "reference",
                                "documentation": "患者參考"
                            },
                            {
                                "name": "code",
                                "type": "token",
                                "documentation": "觀察項目代碼"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    output_path = os.path.join(OUTPUT_DIR, "metadata.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(capability, f, ensure_ascii=False, indent=2)
    
    return capability

def create_code_systems():
    """創建代碼系統資源"""
    code_systems = [
        {
            "resourceType": "CodeSystem",
            "id": "tmu-alzheimers-diagnosis",
            "url": "http://tmu.edu.tw/fhir/alzheimers/diagnosis",
            "version": "1.0.0",
            "name": "TaiwanAlzheimersDiagnosis",
            "title": "臺灣失智症診斷代碼系統",
            "status": "active",
            "content": "complete",
            "concept": [
                {
                    "code": "AD",
                    "display": "阿茲海默症"
                },
                {
                    "code": "VD",
                    "display": "血管性失智症"
                },
                {
                    "code": "MCI",
                    "display": "輕度認知障礙"
                }
            ]
        },
        {
            "resourceType": "CodeSystem",
            "id": "tmu-alzheimers-severity",
            "url": "http://tmu.edu.tw/fhir/alzheimers/dementia-severity",
            "version": "1.0.0",
            "name": "TaiwanAlzheimersSeverity",
            "title": "臺灣失智症嚴重程度代碼系統",
            "status": "active",
            "content": "complete",
            "concept": [
                {
                    "code": "0.5",
                    "display": "極輕度"
                },
                {
                    "code": "1",
                    "display": "輕度"
                },
                {
                    "code": "2",
                    "display": "中度"
                },
                {
                    "code": "3",
                    "display": "重度"
                }
            ]
        }
    ]
    
    for code_system in code_systems:
        output_path = os.path.join(OUTPUT_DIR, f"codesystem-{code_system['id']}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(code_system, f, ensure_ascii=False, indent=2)
    
    return code_systems

def main():
    """主函數"""
    print("開始將 CSV 資料轉換為 FHIR 格式...")
    
    # 獲取所有 CSV 檔案
    csv_files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"在 {DATA_DIR} 中找不到 CSV 檔案")
        return
    
    print(f"找到 {len(csv_files)} 個 CSV 檔案")
    
    # 處理每個 CSV 檔案
    results = []
    for file_path in csv_files:
        result = process_csv_file(file_path)
        results.append(result)
    
    # 創建能力聲明
    print("創建 CapabilityStatement 資源...")
    create_capability_statement()
    
    # 創建代碼系統
    print("創建 CodeSystem 資源...")
    create_code_systems()
    
    # 輸出處理結果
    success_count = sum(1 for r in results if r["status"] == "success")
    error_count = sum(1 for r in results if r["status"] == "error")
    
    print(f"FHIR 轉換處理完成")
    print(f"成功處理: {success_count} 個檔案")
    print(f"處理失敗: {error_count} 個檔案")
    print(f"FHIR 資源已保存至: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
