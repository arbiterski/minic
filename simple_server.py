#!/usr/bin/env python3
"""
簡化版阿茲海默症分析資料庫 - Web 服務器
"""

import os
import json
import hashlib
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 使用非互動式後端
import matplotlib.pyplot as plt
import numpy as np

# 配置
DATASET_PATH = "data/alzheimers_cohort_v1"
DATASET_FILE = "113.csv"
ARTIFACT_DIR = "artifacts"
CLAUDE_SERVER_URL = "http://localhost:3000"

app = Flask(__name__)

class SimpleAnalysisService:
    """簡化版分析服務"""
    
    def __init__(self):
        self.server_url = CLAUDE_SERVER_URL
        self.jobs = {}
    
    def _append_log(self, job_id: str, message: str) -> None:
        """添加日誌"""
        job = self.jobs.get(job_id)
        if job is None:
            return
        logs = job.setdefault('logs', [])
        timestamp = datetime.now().strftime('%H:%M:%S')
        line = f"[{timestamp}] {message}"
        logs.append(line)
        print(f"[{job_id}] {line}")

    def generate_code(self, question: str, outputs: List[str], privacy_level: str) -> Dict[str, Any]:
        """生成 Python 程式碼"""
        
        try:
            # 嘗試呼叫 Claude Code Server
            message = f"""
請為以下阿茲海默症資料分析問題生成 Python 程式碼：

問題：{question}
隱私等級：{privacy_level}
期望輸出：{', '.join(outputs)}

要求：
1. 讀取 CSV 檔案：{DATASET_PATH}/{DATASET_FILE}
2. 生成 {', '.join(outputs)} 輸出
3. 使用 pandas, matplotlib 等庫
4. 將圖表保存到 ARTIFACT_DIR 目錄
5. 只輸出純 Python 程式碼，不要包含 Markdown

資料檔案包含以下欄位：
- 編號, 個案編號, 個案姓名, 性別, 身分證字號, 病歷號
- 生日/年齡, 收案日期, 失智程度, 0.5程度分級
- 失智症診斷, 有無精神行為症狀診斷碼, 主治醫師
- 失智診斷情況負責醫師, 備註, NCV檢查, APOE
            """.strip()
            
            response = requests.post(
                f"{self.server_url}/api/execute",
                headers={"Content-Type": "application/json"},
                json={"message": message, "timeout": 30000},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                code = result.get('result') or result.get('output') or ''
                
                # 清理程式碼
                if isinstance(code, str):
                    code = code.strip()
                    if code.startswith('```'):
                        lines = code.split('\n')
                        if len(lines) > 1:
                            code = '\n'.join(lines[1:-1]) if lines[-1].startswith('```') else '\n'.join(lines[1:])
                    code = code.strip()
                
                code_hash = hashlib.sha256(code.encode()).hexdigest()
                
                return {
                    'code': code,
                    'code_hash': code_hash,
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
        
        # 根據問題類型生成不同的程式碼
        if "性別" in question or "gender" in question.lower():
            code = f'''# 性別分布分析
import pandas as pd
import matplotlib.pyplot as plt

# 讀取資料
df = pd.read_csv('{DATASET_PATH}/{DATASET_FILE}')
print(f"資料集大小: {{df.shape}}")
print(f"欄位: {{list(df.columns)}}")

# 性別分布統計
gender_counts = df['性別'].value_counts()
print("性別分布:")
print(gender_counts)

# 生成圖表
plt.figure(figsize=(8, 6))
gender_counts.plot(kind='bar', color=['lightblue', 'lightcoral'])
plt.title('病患性別分布')
plt.xlabel('性別')
plt.ylabel('人數')
plt.xticks(rotation=0)
plt.tight_layout()

# 保存圖表
plt.savefig(f"{{ARTIFACT_DIR}}/性別分布圖.png", dpi=300, bbox_inches='tight')
plt.close()

# 生成統計摘要
summary = gender_counts.to_frame(name='人數')
summary['百分比'] = (summary['人數'] / len(df) * 100).round(2)
summary.to_csv(f"{{ARTIFACT_DIR}}/性別分布統計.csv", encoding='utf-8-sig')

print("分析完成！")
'''
        elif "年齡" in question or "age" in question.lower():
            code = f'''# 年齡分布分析
import pandas as pd
import matplotlib.pyplot as plt

# 讀取資料
df = pd.read_csv('{DATASET_PATH}/{DATASET_FILE}')
print(f"資料集大小: {{df.shape}}")

# 年齡欄位處理
age_col = '生日/年齡'
if age_col in df.columns:
    # 轉換年齡為數值
    df['年齡數值'] = pd.to_numeric(df[age_col], errors='coerce')
    age_data = df['年齡數值'].dropna()
    age_data = age_data[(age_data > 0) & (age_data < 120)]
    
    print(f"有效年齡資料: {{len(age_data)}} 筆")
    print(f"年齡範圍: {{age_data.min():.1f}} - {{age_data.max():.1f}}")
    
    # 生成年齡分布圖
    plt.figure(figsize=(10, 6))
    plt.hist(age_data, bins=20, alpha=0.7, color='steelblue', edgecolor='white')
    plt.title('病患年齡分布')
    plt.xlabel('年齡')
    plt.ylabel('人數')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # 保存圖表
    plt.savefig(f"{{ARTIFACT_DIR}}/年齡分布圖.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # 生成統計摘要
    stats = age_data.describe()
    stats.to_csv(f"{{ARTIFACT_DIR}}/年齡統計摘要.csv", encoding='utf-8-sig')
    
    print("年齡分析完成！")
else:
    print("找不到年齡欄位")
'''
        else:
            # 通用分析程式碼
            code = f'''# 通用資料分析
import pandas as pd
import matplotlib.pyplot as plt

# 讀取資料
df = pd.read_csv('{DATASET_PATH}/{DATASET_FILE}')
print(f"資料集大小: {{df.shape}}")
print(f"欄位: {{list(df.columns)}}")

# 基本統計
print("\\n基本統計:")
print(df.describe())

# 生成欄位分布圖
plt.figure(figsize=(12, 8))
for i, col in enumerate(df.select_dtypes(include=['object']).columns[:4]):
    plt.subplot(2, 2, i+1)
    df[col].value_counts().head(10).plot(kind='bar')
    plt.title(f'{{col}} 分布')
    plt.xticks(rotation=45)
    plt.tight_layout()

# 保存圖表
plt.savefig(f"{{ARTIFACT_DIR}}/資料分析圖.png", dpi=300, bbox_inches='tight')
plt.close()

# 生成摘要
summary = df.describe()
summary.to_csv(f"{{ARTIFACT_DIR}}/資料摘要.csv", encoding='utf-8-sig')

print("\\n分析完成！")
'''
        
        code_hash = hashlib.sha256(code.encode()).hexdigest()
        return {
            'code': code,
            'code_hash': code_hash,
            'source': 'default_code'
        }
    
    def execute_code(self, code: str, job_id: str) -> Dict[str, Any]:
        """執行 Python 程式碼"""
        
        try:
            # 創建 artifacts 目錄
            artifacts_dir = Path(ARTIFACT_DIR) / job_id
            artifacts_dir.mkdir(parents=True, exist_ok=True)
            
            # 設置執行環境
            exec_globals = {
                '__builtins__': __builtins__,
                '__name__': '__main__',
                '__file__': f'analysis_{job_id}.py',
                'ARTIFACT_DIR': str(artifacts_dir),
                'pd': pd,
                'plt': plt,
                'np': np
            }
            
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
    
    def create_analysis(self, question: str, outputs: List[str], privacy_level: str) -> str:
        """創建分析工作"""
        
        job_id = f"job_{len(self.jobs) + 1}_{int(datetime.now().timestamp())}"
        
        # 初始化工作
        self.jobs[job_id] = {
            'question': question,
            'outputs': outputs,
            'privacy_level': privacy_level,
            'code_hash': '',
            'execution_result': {'status': 'processing', 'artifacts': []},
            'created_at': datetime.now().isoformat(),
            'code': '',
            'logs': []
        }
        
        self._append_log(job_id, '收到分析請求')
        self._append_log(job_id, '正在生成分析程式碼')
        
        # 生成程式碼
        code_result = self.generate_code(question, outputs, privacy_level)
        self.jobs[job_id]['code'] = code_result['code']
        self.jobs[job_id]['code_hash'] = code_result['code_hash']
        self._append_log(job_id, f"程式碼來源: {code_result.get('source', 'unknown')}")
        
        # 執行程式碼
        self._append_log(job_id, '開始執行分析程式碼')
        execution_result = self.execute_code(code_result['code'], job_id)
        self.jobs[job_id]['execution_result'] = execution_result
        
        if execution_result.get('status') == 'success':
            artifacts = execution_result.get('artifacts', [])
            self._append_log(job_id, f"分析完成，產出檔案: {', '.join(artifacts) if artifacts else '無'}")
        else:
            self._append_log(job_id, f"分析失敗: {execution_result.get('error', '未知錯誤')}")
        
        return job_id
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """獲取工作狀態"""
        job = self.jobs.get(job_id)
        if job is None:
            return {'error': '工作不存在'}
        
        # 補上 job_id 方便前端組裝檔案連結
        return {'job_id': job_id, **job}
    
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

# 創建服務實例
analysis_service = SimpleAnalysisService()

@app.route('/')
def index():
    """主頁面"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """分析 API 端點"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        outputs = data.get('outputs', ['plot', 'summary'])
        privacy_level = data.get('privacy_level', 'medium')
        
        if not question:
            return jsonify({'error': '問題不能為空'}), 400
        
        # 創建分析工作
        job_id = analysis_service.create_analysis(question, outputs, privacy_level)
        
        return jsonify({
            'job_id': job_id,
            'message': '分析工作已創建',
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/job/<job_id>')
def get_job(job_id):
    """獲取工作狀態"""
    job_status = analysis_service.get_job_status(job_id)
    return jsonify(job_status)

@app.route('/api/jobs')
def list_jobs():
    """列出所有工作"""
    jobs = analysis_service.list_jobs()
    return jsonify(jobs)

@app.route('/files/<job_id>/<filename>')
def get_file(job_id, filename):
    """獲取生成的文件"""
    file_path = Path(ARTIFACT_DIR) / job_id / filename
    if file_path.exists():
        return send_from_directory(Path(ARTIFACT_DIR) / job_id, filename)
    else:
        return jsonify({'error': '文件不存在'}), 404

@app.route('/health')
def health():
    """健康檢查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'claude_server': CLAUDE_SERVER_URL
    })

if __name__ == '__main__':
    # 檢查資料檔案
    csv_file = Path(DATASET_PATH) / DATASET_FILE
    if not csv_file.exists():
        print(f"❌ 找不到資料檔案: {csv_file}")
        print("   請確保 CSV 檔案已放置在正確位置")
        exit(1)
    
    print(f"✅ 找到資料檔案: {csv_file}")
    print("🌐 啟動簡化版 Web 服務器...")
    print("📱 訪問: http://localhost:5001")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
