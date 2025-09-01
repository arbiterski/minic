#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿茲海默症分析資料庫 - Web 服務器
"""

import os
import re
import json
import hashlib
import requests
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 配置
DATASET_PATH = "data/alzheimers_cohort_v1"
DATASET_FILE = "113.csv"  # 使用 113.csv 檔案
ARTIFACT_DIR = "artifacts"
CLAUDE_SERVER_URL = "http://localhost:3000"

app = Flask(__name__)

class WebClaudeService:
    """Web 版本的 Claude 服務"""
    
    def __init__(self):
        self.server_url = CLAUDE_SERVER_URL
        self.jobs = {}
    
    def _append_log(self, job_id, message):
        job = self.jobs.get(job_id)
        if job is None:
            return
        logs = job.setdefault('logs', [])
        timestamp = datetime.now().strftime('%H:%M:%S')
        line = "[{}] {}".format(timestamp, message)
        logs.append(line)
        # 同步輸出到終端機
        print("[job {}] {}".format(job_id, line))

    def _slugify(self, text, default='artifact'):
        if not text:
            return default
        # keep CJK and alnum, replace others with underscore, then trim
        text = re.sub(r"[^\w\u4e00-\u9fff]+", "_", text)
        text = re.sub(r"_+", "_", text).strip("_")
        return (text or default)[:64]
    
    def generate_code(self, question, outputs, privacy_level):
        """生成 Python 程式碼"""
        
        try:
            # 構建請求訊息
            message = """
請為以下阿茲海默症資料分析問題生成 Python 程式碼：

問題：{}
隱私等級：{}
期望輸出：{}

要求：
1. 讀取 CSV 檔案：{}/{}
2. 生成 {} 輸出
3. 應用 {} 隱私保護
4. 使用 pandas, matplotlib 等庫
5. 將圖表保存到 {}/ 目錄
6. 返回可執行的 Python 程式碼

資料檔案包含以下欄位：
- 編號, 個案編號, 個案姓名, 性別, 身分證字號, 病歷號
- 生日/年齡, 收案日期, 失智程度, 0.5程度分級
- 失智症診斷, 有無精神行為症狀診斷碼, 主治醫師
- 失智診斷情況負責醫師, 備註, NCV檢查, APOE

輸出格式要求（重要）：
- 只輸出純 Python 程式碼，且不要包含 Markdown、不要包含```標記、不要任何解說文字。
- 程式碼中直接使用變數 ARTIFACT_DIR 作為輸出目錄。
            """.format(question, privacy_level, ', '.join(outputs), DATASET_PATH, DATASET_FILE, ', '.join(outputs), privacy_level, ARTIFACT_DIR).strip()
            
            # 發送請求到 Claude Code Server
            response = requests.post(
                "{}/api/execute".format(self.server_url),
                headers={"Content-Type": "application/json"},
                json={
                    "message": message,
                    "timeout": 30000
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                # 兼容不同欄位名（部分服務回傳 output）
                code = result.get('result') or result.get('output') or ''
                # 去除可能的 Markdown 程式碼圍欄
                if isinstance(code, str):
                    stripped = code.strip()
                    if stripped.startswith('```'):
                        # 去除開頭的```語法與可選語言標籤
                        stripped = stripped.lstrip('`')
                        # 再次保守處理：移除可能的開頭 'python' 換行
                        if '\n' in stripped:
                            stripped = stripped.split('\n', 1)[1]
                        # 去除結尾的```
                        stripped = stripped.rstrip('`').strip()
                    code = stripped
                
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
                raise Exception("Claude Code Server 回應錯誤: {}".format(response.status_code))
                
        except Exception as e:
            print("Claude Code Server 調用失敗: {}".format(e))
            # 返回預設程式碼
            return self._generate_default_code(question, outputs, privacy_level)
    
    def _generate_default_code(self, question, outputs, privacy_level):
        """生成預設程式碼"""
        
        code = '''# 生成程式碼: {}
# 隱私等級: {}
# 輸出類型: {}

import pandas as pd
import matplotlib.pyplot as plt

# 讀取 CSV 資料
df = pd.read_csv('{}/{}')

# 基本統計
        print("資料集大小: {}".format(df.shape))
        print("欄位: {}".format(list(df.columns)))

# 生成輸出
'''.format(question, privacy_level, ', '.join(outputs), DATASET_PATH, DATASET_FILE)
        
        if "plot" in outputs:
            code += '''
# 資料前處理：欄位統一與年齡欄位辨識
df.columns = [str(c).replace(' ', '') for c in df.columns]
age_candidates = ['生日/年齡', '生日/年齡', '生日/年齡', '生日/年齡', '生日/年齡']
age_candidates = list(dict.fromkeys(age_candidates + ['生日/年齡','生日/年齡','年齡']))
age_col = None
for c in df.columns:
    if '年齡' in c:
        age_col = c
        break
if age_col is None:
    age_col = '生日/年齡' if '生日/年齡' in df.columns else df.columns[0]

# 年齡轉數值並清理
age_series = pd.to_numeric(df[age_col], errors='coerce').dropna()
age_series = age_series[(age_series > 0) & (age_series < 120)]

# 畫出年齡分布圖（直方圖）
plt.figure(figsize=(10, 6))
age_series.hist(bins=20, alpha=0.8, color='steelblue', edgecolor='white')
plt.title('病患年齡分布')
plt.xlabel('年齡')
plt.ylabel('人數')
plt.tight_layout()
outfile = "{}/{}_{}_plot.png".format(ARTIFACT_DIR, ARTIFACT_BASENAME, job_id)
plt.savefig(outfile, dpi=300, bbox_inches='tight')
plt.close()
'''
        
        if "table" in outputs:
            code += '''
# 生成年齡統計表格
age_stats = age_series.describe().to_frame(name='age')

# 依區間統計分布
bins = [0, 50, 60, 70, 80, 90, 120]
labels = ['<50','50-59','60-69','70-79','80-89','90+']
age_bins = pd.cut(age_series, bins=bins, labels=labels, right=False)
age_bin_counts = age_bins.value_counts().sort_index().to_frame(name='count')

summary = pd.concat([age_stats, age_bin_counts], axis=1)
summary.to_csv("{}/{}_{}_summary.csv".format(ARTIFACT_DIR, ARTIFACT_BASENAME, job_id))
'''
        
        if "explanation" in outputs:
            code += '''
# 生成分析說明
explanation = "資料集包含 {} 筆記錄，{} 個欄位。".format(len(df), len(df.columns))
with open('{}/explanation.txt'.format(ARTIFACT_DIR), 'w', encoding='utf-8') as f:
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
    
    def execute_code(self, code, job_id):
        """執行 Python 程式碼"""
        
        try:
            # 創建 artifacts 目錄
            artifacts_dir = Path(ARTIFACT_DIR) / job_id
            artifacts_dir.mkdir(parents=True, exist_ok=True)
            
            # 設置環境變數
            os.environ['ARTIFACT_DIR'] = str(artifacts_dir)
            
            # 執行程式碼
            exec_globals = {
                '__builtins__': __builtins__,
                '__name__': '__main__',
                '__file__': 'analysis_{}.py'.format(job_id),
                'ARTIFACT_DIR': str(artifacts_dir)  # 添加 ARTIFACT_DIR 變數
            }
            
            # 添加必要的模組
            try:
                import pandas as pd
                import matplotlib
                matplotlib.use('Agg')  # 使用非互動式後端
                import matplotlib.pyplot as plt
                # 設定可顯示中文的字型（macOS 優先 PingFang，其次 Noto/Arial Unicode）
                try:
                    matplotlib.rcParams['font.sans-serif'] = [
                        'PingFang TC', 'PingFang HK', 'PingFang SC',
                        'Noto Sans CJK TC', 'Noto Sans CJK SC', 'Noto Sans CJK JP',
                        'Heiti TC', 'Hiragino Sans GB', 'Arial Unicode MS', 'Songti SC', 'STHeiti'
                    ]
                    matplotlib.rcParams['axes.unicode_minus'] = False
                except Exception:
                    pass
                import numpy as np
                # 將任務標題提供給代碼使用（可自訂輸出檔名）
                job_meta = self.jobs.get(job_id, {})
                artifact_basename = job_meta.get('artifact_basename', 'artifact')
                exec_globals.update({
                    'pd': pd,
                    'plt': plt,
                    'np': np,
                    'df': None,  # 將在程式碼中設置
                    'ARTIFACT_BASENAME': artifact_basename
                })
            except ImportError as e:
                return {'status': 'error', 'error': '模組導入失敗: {}'.format(e)}
            
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
    
    def create_analysis(self, question, outputs, privacy_level):
        """創建分析工作"""
        
        job_id = "job_{}_{}".format(len(self.jobs) + 1, int(datetime.now().timestamp()))
        # 初始化工作（先寫入，以便即時追加日誌）
        artifact_basename = self._slugify(question)
        self.jobs[job_id] = {
            'question': question,
            'outputs': outputs,
            'privacy_level': privacy_level,
            'code_hash': '',
            'execution_result': {'status': 'processing', 'artifacts': []},
            'created_at': datetime.now().isoformat(),
            'code': '',
            'logs': [],
            'artifact_basename': artifact_basename
        }
        
        self._append_log(job_id, '收到分析請求')
        self._append_log(job_id, '正在呼叫 Claude Code Server 產生程式碼')
        
        # 生成程式碼
        code_result = self.generate_code(question, outputs, privacy_level)
        self.jobs[job_id]['code'] = code_result['code']
        self.jobs[job_id]['code_hash'] = code_result['code_hash']
        self._append_log(job_id, "程式碼來源: {}".format(code_result.get('source', 'unknown')))
        
        # 執行程式碼
        self._append_log(job_id, '開始執行分析程式碼')
        execution_result = self.execute_code(code_result['code'], job_id)
        self.jobs[job_id]['execution_result'] = execution_result
        
        if execution_result.get('status') == 'success':
            artifacts = execution_result.get('artifacts', [])
            self._append_log(job_id, "分析完成，產出檔案: {}".format(', '.join(artifacts) if artifacts else '無'))
        else:
            self._append_log(job_id, "分析失敗: {}".format(execution_result.get('error', '未知錯誤')))
        
        return job_id
    
    def get_job_status(self, job_id):
        """獲取工作狀態"""
        return self.jobs.get(job_id, {'error': '工作不存在'})
    
    def list_jobs(self):
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
claude_service = WebClaudeService()

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
        outputs = data.get('outputs', ['plot', 'table'])
        privacy_level = data.get('privacy_level', 'k_anonymous')
        
        if not question:
            return jsonify({'error': '問題不能為空'}), 400
        
        # 創建分析工作
        job_id = claude_service.create_analysis(question, outputs, privacy_level)
        
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
    job_status = claude_service.get_job_status(job_id)
    # 若工作存在，補上 job_id 方便前端組裝檔案連結
    if 'error' not in job_status:
        job_status_with_id = { 'job_id': job_id, **job_status }
        return jsonify(job_status_with_id)
    return jsonify(job_status)

@app.route('/api/jobs')
def list_jobs():
    """列出所有工作"""
    jobs = claude_service.list_jobs()
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
        'claude_server': 'http://localhost:3000'
    })

@app.route('/download/<filename>')
def download_file(filename):
    """下載檔案"""
    try:
        # 只允許下載去識別化的 CSV 檔案
        if filename == 'anonymized_csv.zip':
            file_path = Path('static/downloads') / filename
            if file_path.exists():
                return send_from_directory('static/downloads', filename, as_attachment=True)
            else:
                return jsonify({'error': '檔案不存在'}), 404
        else:
            return jsonify({'error': '不允許下載此檔案'}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-info')
def get_download_info():
    """獲取下載資訊"""
    try:
        info_path = Path('static/downloads/download_info.json')
        if info_path.exists():
            with open(info_path, 'r', encoding='utf-8') as f:
                info = json.load(f)
            return jsonify(info)
        else:
            return jsonify({'error': '下載資訊不存在'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/about')
def about():
    """關於頁面"""
    return render_template('about.html')

@app.route('/database/<database_name>')
def database_detail(database_name):
    """資料庫詳情頁面"""
    if database_name == 'dementia':
        database = {
            'title': '臺灣失智症臨床資料庫',
            'authors': '臺北醫學大學雙和醫院失智症中心與神經內科研究團隊',
            'publication_date': '2025年8月28日',
            'version': '1.0.0',
            'abstract': '這項研究採用臺北醫學大學雙和醫院失智症中心與神經內科的受試者資料，建立了以阿茲海默症患者為核心的臨床資料庫。該資料庫收錄符合美國國家老化研究院-阿茲海默症協會(NIA-AA)標準的疑似AD患者，收集的內容包含病歷、神經心理評估（如MMSE、CASI、CDR）、持續多年的追蹤數據及部分患者的腦部MRI影像。所有數據經過嚴格去識別化處理，並遵照研究倫理規範，包含人口統計、病程、教育年數、神經心理多領域測驗分數、臨床失智嚴重度、腦萎縮與白質病灶評分等詳細變項。',
            'background': '該資料庫的患者涵蓋輕至中度阿茲海默症，具備多次年度評估紀錄與完整隨訪資料。研究團隊將神經心理評估各面向結合機器學習方法進行異質性分類，促進亞型分群分析。',
            'methods': '資料收集採用標準化神經心理評估工具，包括MMSE、CASI、CDR等量表。所有數據經過嚴格去識別化處理，確保患者隱私保護。',
            'data_description': '資料庫包含多個CSV檔案，涵蓋患者基本資訊、診斷結果、認知測試分數、腦部影像評分等。',
            'usage_notes': '本資料庫僅供研究使用，使用者需遵守相關倫理規範和資料使用協議。',
            'release_notes': '初始版本包含2012-2024年收案資料，經過去識別化處理後發布。',
            'ethics': '本研究已通過臺北醫學大學人體試驗委員會審查，所有參與者均簽署知情同意書。',
            'acknowledgements': '感謝所有參與研究的患者及其家屬，以及研究團隊成員的貢獻。',
            'conflicts_of_interest': '研究團隊聲明無利益衝突。',
            'references': [
                'Nguyen TTT, Lee HH, Huang LK, et al. Heterogeneity of Alzheimer\'s disease identified by neuropsychological test profiling. PLoS One. 2023;18(10):e0292527. https://pubmed.ncbi.nlm.nih.gov/37797059/',
                'American Psychiatric Association. Diagnostic and Statistical Manual of Mental Disorders, Fifth Edition (DSM-5). Arlington, VA: American Psychiatric Association, 2013.',
                'McKhann GM, et al. The diagnosis of dementia due to Alzheimer\'s disease: recommendations from the National Institute on Aging-Alzheimer\'s Association workgroups on diagnostic guidelines for Alzheimer\'s disease. Alzheimers Dement. 2011;7(3):263-9.',
                'Folstein MF, Folstein SE, McHugh PR. "Mini-mental state". A practical method for grading the cognitive state of patients for the clinician. J Psychiatr Res. 1975;12(3):189-98.'
            ],
            'access_policy': '開放存取，需註冊帳號並同意使用條款。',
            'license': 'Creative Commons Attribution 4.0 International License',
            'doi': '10.1371/journal.pone.0292527',
            'topics': ['阿茲海默症', '神經心理評估', '認知功能', '機器學習', '異質性分析'],
            'project_website': 'https://neurologytmu.loinc100.org',
            'total_size': '213.29 KB',
            'zip_size': '213.29 KB',
            'download_url': '/download/anonymized_csv.zip',
            'wget_command': 'wget http://localhost:5001/download/anonymized_csv.zip',
            'versions': [
                {'number': '1.0.0', 'date': '2025年8月28日'}
            ]
        }
        return render_template('database_detail.html', database=database)
    else:
        return jsonify({'error': '資料庫不存在'}), 404

if __name__ == '__main__':
    # 檢查資料檔案
    csv_file = Path(DATASET_PATH) / DATASET_FILE
    if not csv_file.exists():
        print("❌ 找不到資料檔案: {}".format(csv_file))
        print("   請確保 CSV 檔案已放置在正確位置")
        exit(1)
    
    print("✅ 找到資料檔案: {}".format(csv_file))
    print("🌐 啟動 Web 服務器...")
    print("📱 訪問: http://localhost:5001")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
