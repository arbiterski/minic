#!/usr/bin/env python3
"""
簡化的阿茲海默症分析資料庫 - 本地運行版本
"""

import os
import sys
import json
import hashlib
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# 配置
DATASET_PATH = "data/alzheimers_cohort_v1"
ARTIFACT_DIR = "artifacts"
CLAUDE_SERVER_URL = "http://localhost:3000"

class SimpleClaudeService:
    """簡化的 Claude 服務"""
    
    def __init__(self):
        self.server_url = CLAUDE_SERVER_URL
    
    def generate_code(self, question: str, outputs: List[str], privacy_level: str) -> Dict[str, Any]:
        """生成 Python 程式碼"""
        
        try:
            # 構建請求訊息
            message = f"""
請為以下阿茲海默症資料分析問題生成 Python 程式碼：

問題：{question}
隱私等級：{privacy_level}
期望輸出：{', '.join(outputs)}

要求：
1. 讀取 Excel 檔案：{DATASET_PATH}/patients.xlsx
2. 生成 {', '.join(outputs)} 輸出
3. 應用 {privacy_level} 隱私保護
4. 使用 pandas, matplotlib, openpyxl 等庫
5. 將圖表保存到 {ARTIFACT_DIR}/ 目錄
6. 返回可執行的 Python 程式碼
            """.strip()
            
            # 發送請求到 Claude Code Server
            response = requests.post(
                f"{self.server_url}/api/execute",
                headers={"Content-Type": "application/json"},
                json={
                    "message": message,
                    "timeout": 30000
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                code = result.get('result', '')
                
                # 生成程式碼雜湊
                code_hash = hashlib.sha256(code.encode()).hexdigest()
                
                return {
                    'code': code,
                    'code_hash': code_hash,
                    'question': question,
                    'outputs': outputs,
                    'privacy_level': privacy_level,
                    'source': 'claude_code_server'
                }
            else:
                raise Exception(f"Claude Code Server 回應錯誤: {response.status_code}")
                
        except Exception as e:
            print(f"Claude Code Server 調用失敗: {e}")
            # 返回預設程式碼
            return self._generate_default_code(question, outputs, privacy_level)
    
    def _generate_default_code(self, question: str, outputs: List[str], privacy_level: str) -> Dict[str, Any]:
        """生成預設程式碼"""
        
        code = f'''# 生成程式碼: {question}
# 隱私等級: {privacy_level}
# 輸出類型: {', '.join(outputs)}

import pandas as pd
import matplotlib.pyplot as plt

# 讀取 Excel 資料
df = pd.read_excel('{DATASET_PATH}/patients.xlsx')

# 基本統計
print(f"資料集大小: {{df.shape}}")
print(f"欄位: {{list(df.columns)}}")

# 生成輸出
'''
        
        if "plot" in outputs:
            code += '''
# 生成圖表
plt.figure(figsize=(10, 6))
df['age'].hist(bins=20, alpha=0.7)
plt.title('病患年齡分布')
plt.xlabel('年齡')
plt.ylabel('頻率')
plt.savefig(f'{ARTIFACT_DIR}/age_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
'''
        
        if "table" in outputs:
            code += '''
# 生成統計表格
summary = df.describe()
summary.to_csv(f'{ARTIFACT_DIR}/summary_stats.csv')
'''
        
        if "explanation" in outputs:
            code += '''
# 生成分析說明
explanation = f"資料集包含 {{len(df)}} 筆記錄，{len(df.columns)} 個欄位。"
with open(f'{ARTIFACT_DIR}/explanation.txt', 'w', encoding='utf-8') as f:
    f.write(explanation)
'''
        
        code_hash = hashlib.sha256(code.encode()).hexdigest()
        
        return {
            'code': code,
            'code_hash': code_hash,
            'question': question,
            'outputs': outputs,
            'privacy_level': privacy_level,
            'source': 'default'
        }

class SimpleAnalysisService:
    """簡化的分析服務"""
    
    def __init__(self):
        self.claude_service = SimpleClaudeService()
        self.jobs = {}
    
    def create_analysis(self, question: str, outputs: List[str], privacy_level: str) -> str:
        """創建分析工作"""
        
        job_id = f"job_{len(self.jobs) + 1}_{int(datetime.now().timestamp())}"
        
        print(f"🎯 創建分析工作: {job_id}")
        print(f"📝 問題: {question}")
        print(f"📊 輸出: {', '.join(outputs)}")
        print(f"🔒 隱私等級: {privacy_level}")
        
        # 生成程式碼
        print("\n🤖 正在生成 Python 程式碼...")
        code_result = self.claude_service.generate_code(question, outputs, privacy_level)
        
        print(f"✅ 程式碼生成成功")
        print(f"   來源: {code_result['source']}")
        print(f"   程式碼雜湊: {code_result['code_hash'][:16]}...")
        
        # 執行程式碼
        print("\n🚀 正在執行程式碼...")
        execution_result = self._execute_code(code_result['code'], job_id)
        
        # 保存工作結果
        self.jobs[job_id] = {
            'question': question,
            'outputs': outputs,
            'privacy_level': privacy_level,
            'code_hash': code_result['code_hash'],
            'execution_result': execution_result,
            'created_at': datetime.now().isoformat()
        }
        
        print(f"\n🎉 分析工作完成: {job_id}")
        return job_id
    
    def _execute_code(self, code: str, job_id: str) -> Dict[str, Any]:
        """執行 Python 程式碼"""
        
        try:
            # 創建 artifacts 目錄
            artifacts_dir = Path(ARTIFACT_DIR) / job_id
            artifacts_dir.mkdir(parents=True, exist_ok=True)
            
            # 設置環境變數
            os.environ['ARTIFACT_DIR'] = str(artifacts_dir)
            
            # 執行程式碼
            exec_globals = {
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'list': list,
                    'str': str,
                    'int': int,
                    'float': float,
                    'dict': dict,
                    'list': list,
                    'tuple': tuple,
                    'set': set,
                    'frozenset': frozenset,
                    'bool': bool,
                    'bytes': bytes,
                    'bytearray': bytearray,
                    'memoryview': memoryview,
                    'complex': complex,
                    'range': range,
                    'slice': slice,
                    'type': type,
                    'object': object,
                    'property': property,
                    'staticmethod': staticmethod,
                    'classmethod': classmethod,
                    'super': super,
                    'enumerate': enumerate,
                    'zip': zip,
                    'filter': filter,
                    'map': map,
                    'reversed': reversed,
                    'sorted': sorted,
                    'any': any,
                    'all': all,
                    'min': min,
                    'max': max,
                    'sum': sum,
                    'abs': abs,
                    'round': round,
                    'pow': pow,
                    'divmod': divmod,
                    'bin': bin,
                    'oct': oct,
                    'hex': hex,
                    'chr': chr,
                    'ord': ord,
                    'hash': hash,
                    'id': id,
                    'isinstance': isinstance,
                    'issubclass': issubclass,
                    'callable': callable,
                    'getattr': getattr,
                    'setattr': setattr,
                    'delattr': delattr,
                    'hasattr': hasattr,
                    'vars': vars,
                    'dir': dir,
                    'globals': globals,
                    'locals': locals,
                    'eval': eval,
                    'exec': exec,
                    'compile': compile,
                    'open': open,
                    'input': input,
                    'format': format,
                    'repr': repr,
                    'ascii': ascii,
                    'breakpoint': breakpoint,
                }
            }
            
            # 添加必要的模組
            try:
                import pandas as pd
                import matplotlib.pyplot as plt
                import numpy as np
                exec_globals.update({
                    'pd': pd,
                    'plt': plt,
                    'np': np,
                    'df': None  # 將在程式碼中設置
                })
            except ImportError as e:
                print(f"⚠️  模組導入失敗: {e}")
                print("   請安裝必要的套件: pip install pandas matplotlib numpy openpyxl")
                return {'status': 'error', 'error': f'模組導入失敗: {e}'}
            
            # 執行程式碼
            exec(code, exec_globals)
            
            # 檢查生成的檔案
            artifacts = []
            if artifacts_dir.exists():
                for file_path in artifacts_dir.iterdir():
                    if file_path.is_file():
                        artifacts.append(file_path.name)
            
            return {
                'status': 'success',
                'artifacts': artifacts,
                'message': '程式碼執行成功'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'artifacts': []
            }
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """獲取工作狀態"""
        return self.jobs.get(job_id, {'error': '工作不存在'})
    
    def list_jobs(self) -> List[Dict[str, Any]]:
        """列出所有工作"""
        return [
            {
                'job_id': job_id,
                'question': job_info['question'],
                'status': 'completed',
                'created_at': job_info['created_at'],
                'artifacts': job_info['execution_result'].get('artifacts', [])
            }
            for job_id, job_info in self.jobs.items()
        ]

def main():
    """主函數"""
    
    print("🧠 阿茲海默症分析資料庫 - 簡化版本")
    print("=" * 50)
    
    # 檢查資料檔案
    excel_file = Path(DATASET_PATH) / "patients.xlsx"
    if not excel_file.exists():
        print(f"❌ 找不到資料檔案: {excel_file}")
        print("   請確保 Excel 檔案已放置在正確位置")
        return
    
    print(f"✅ 找到資料檔案: {excel_file}")
    
    # 創建服務
    service = SimpleAnalysisService()
    
    # 測試問題
    test_questions = [
        ("歷年病患分布折線圖", ["plot", "table"]),
        ("病患年齡分布統計", ["plot", "table", "explanation"]),
        ("性別與教育程度比較", ["plot", "table"])
    ]
    
    print(f"\n🚀 開始分析測試...")
    
    for i, (question, outputs) in enumerate(test_questions, 1):
        print(f"\n📝 測試 {i}: {question}")
        print("-" * 40)
        
        try:
            job_id = service.create_analysis(question, outputs, "k_anonymous")
            
            # 顯示結果
            job_status = service.get_job_status(job_id)
            if job_status['execution_result']['status'] == 'success':
                artifacts = job_status['execution_result']['artifacts']
                print(f"✅ 分析完成！生成檔案: {', '.join(artifacts)}")
            else:
                print(f"❌ 分析失敗: {job_status['execution_result']['error']}")
                
        except Exception as e:
            print(f"❌ 測試失敗: {e}")
    
    # 顯示所有工作
    print(f"\n📊 工作摘要:")
    print("-" * 40)
    jobs = service.list_jobs()
    for job in jobs:
        print(f"  {job['job_id']}: {job['question']}")
        print(f"    狀態: {job['status']}")
        print(f"    檔案: {', '.join(job['artifacts'])}")
    
    print(f"\n🎯 測試完成！")
    print(f"📁 結果檔案保存在: {ARTIFACT_DIR}/")

if __name__ == "__main__":
    main()
