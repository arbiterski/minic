"""
Claude Code Server - 負責接收指令並生成 Python 程式碼
"""

import os
import hashlib
import requests
import json
from typing import List, Dict, Any
from app.models.schemas import OutputType, PrivacyLevel
from app.core.config import settings

class ClaudeCodeServer:
    """Claude Code Server 服務"""
    
    def __init__(self):
        self.api_key = settings.anthropic_api_key
        self.model = settings.claude_model
    
    def generate_code(self, question: str, outputs: List[OutputType], privacy_level: PrivacyLevel) -> Dict[str, Any]:
        """
        根據問題生成 Python 程式碼
        
        Args:
            question: 用戶問題 (例如: "歷年病患分布折線圖")
            outputs: 期望輸出類型
            privacy_level: 隱私保護等級
            
        Returns:
            包含程式碼和元資料的字典
        """
        # 優先使用 Claude Code Server
        try:
            return self._call_claude_code_server(question, outputs, privacy_level)
        except Exception as e:
            print(f"Claude Code Server 調用失敗: {e}")
            # 回退到預設程式碼
            return self._generate_default_code(question, outputs, privacy_level)
    
    def _call_claude_code_server(self, question: str, outputs: List[OutputType], privacy_level: PrivacyLevel) -> Dict[str, Any]:
        """調用您的 Claude Code Server"""
        
        # 構建請求訊息
        message = f"""
請為以下阿茲海默症資料分析問題生成 Python 程式碼：

問題：{question}
隱私等級：{privacy_level}
期望輸出：{', '.join(outputs)}

要求：
1. 讀取 Excel 檔案：{settings.dataset_path}/patients.xlsx
2. 生成 {', '.join(outputs)} 輸出
3. 應用 {privacy_level} 隱私保護
4. 使用 pandas, matplotlib, openpyxl 等庫
5. 將圖表保存到 /artifacts/ 目錄
6. 返回可執行的 Python 程式碼
        """.strip()
        
        # 發送請求到 Claude Code Server
        response = requests.post(
            f"{settings.claude_code_server_url}/api/execute",
            headers={"Content-Type": "application/json"},
            json={
                "message": message,
                "timeout": settings.claude_code_server_timeout
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
                'language': 'python',
                'libraries': ['pandas', 'matplotlib', 'openpyxl'],
                'source': 'claude_code_server'
            }
        else:
            raise Exception(f"Claude Code Server 回應錯誤: {response.status_code}")
    
    def _generate_default_code(self, question: str, outputs: List[OutputType], privacy_level: PrivacyLevel) -> Dict[str, Any]:
        """生成預設程式碼用於演示"""
        
        # 根據問題類型生成不同的程式碼
        if "折線圖" in question or "趨勢" in question:
            code = self._generate_trend_chart_code(question, outputs, privacy_level)
        elif "分布" in question or "統計" in question:
            code = self._generate_distribution_code(question, outputs, privacy_level)
        elif "比較" in question or "對比" in question:
            code = self._generate_comparison_code(question, outputs, privacy_level)
        else:
            code = self._generate_general_analysis_code(question, outputs, privacy_level)
        
        # 生成程式碼雜湊
        code_hash = hashlib.sha256(code.encode()).hexdigest()
        
        return {
            'code': code,
            'code_hash': code_hash,
            'question': question,
            'outputs': outputs,
            'privacy_level': privacy_level,
            'language': 'python',
            'libraries': ['pandas', 'matplotlib', 'openpyxl']
        }
    
    def _generate_trend_chart_code(self, question: str, outputs: List[OutputType], privacy_level: PrivacyLevel) -> str:
        """生成趨勢圖表程式碼"""
        
        code = f'''# 生成程式碼: {question}
# 隱私等級: {privacy_level}
# 輸出類型: {', '.join(outputs)}

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# 讀取 Excel 資料
df = pd.read_excel('{settings.dataset_path}/patients.xlsx')

# 資料預處理
df['diagnosis_date'] = pd.to_datetime(df['diagnosis_date'])
df['year'] = df['diagnosis_date'].dt.year

# 按年份統計病患數量
yearly_counts = df.groupby('year').size().reset_index(name='patient_count')

# 隱私保護
if "{privacy_level.value}" == "k_anonymous":
    # 確保 k-匿名性 (k={settings.k_anonymity})
    if len(yearly_counts) < {settings.k_anonymity}:
        yearly_counts = pd.DataFrame()
    else:
        # 聚合資料以確保隱私
        yearly_counts = yearly_counts[yearly_counts['patient_count'] >= {settings.k_anonymity}]

# 生成輸出
'''
        
        if OutputType.PLOT in outputs:
            code += '''
# 生成折線圖
plt.figure(figsize=(12, 6))
if not yearly_counts.empty:
    plt.plot(yearly_counts['year'], yearly_counts['patient_count'], marker='o', linewidth=2, markersize=8)
    plt.title('歷年病患分布趨勢', fontsize=16, fontweight='bold')
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('病患數量', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 保存圖表
    plt.savefig('/artifacts/trend_chart.png', dpi=300, bbox_inches='tight')
    plot = plt.gcf()
else:
    plot = None
    plt.close()
'''
        
        if OutputType.TABLE in outputs:
            code += '''
# 生成統計表格
if not yearly_counts.empty:
    table = yearly_counts.copy()
    table['percentage'] = (table['patient_count'] / table['patient_count'].sum() * 100).round(2)
    table = table.sort_values('year')
else:
    table = pd.DataFrame()
'''
        
        if OutputType.EXPLANATION in outputs:
            code += '''
# 生成分析說明
if not yearly_counts.empty:
    total_patients = yearly_counts['patient_count'].sum()
    max_year = yearly_counts.loc[yearly_counts['patient_count'].idxmax()]
    explanation = f"分析結果顯示，從 {yearly_counts['year'].min()} 年到 {yearly_counts['year'].max()} 年，"
    explanation += f"總共有 {total_patients} 位病患。其中 {max_year['year']} 年的病患數量最多，"
    explanation += f"達到 {max_year['patient_count']} 人。"
else:
    explanation = "由於隱私保護要求，無法顯示詳細的年度分布資料。"
'''
        
        return code
    
    def _generate_distribution_code(self, question: str, outputs: List[OutputType], privacy_level: PrivacyLevel) -> str:
        """生成分布統計程式碼"""
        
        code = f'''# 生成程式碼: {question}
# 隱私等級: {privacy_level}
# 輸出類型: {', '.join(outputs)}

import pandas as pd
import matplotlib.pyplot as plt

# 讀取 Excel 資料
df = pd.read_excel('{settings.dataset_path}/patients.xlsx')

# 基本統計
summary_stats = df.describe()

# 年齡分布
age_distribution = df['age'].value_counts().sort_index()

# 隱私保護
if "{privacy_level.value}" == "k_anonymous":
    if len(df) < {settings.k_anonymity}:
        age_distribution = pd.Series()
    else:
        # 年齡分組以確保隱私
        age_distribution = df.groupby(pd.cut(df['age'], bins=10)).size()

# 生成輸出
'''
        
        if OutputType.PLOT in outputs:
            code += '''
# 生成分布圖
plt.figure(figsize=(12, 6))
if not age_distribution.empty:
    age_distribution.plot(kind='bar')
    plt.title('病患年齡分布', fontsize=16, fontweight='bold')
    plt.xlabel('年齡組', fontsize=12)
    plt.ylabel('病患數量', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.savefig('/artifacts/age_distribution.png', dpi=300, bbox_inches='tight')
    plot = plt.gcf()
else:
    plot = None
    plt.close()
'''
        
        if OutputType.TABLE in outputs:
            code += '''
# 生成統計表格
if not age_distribution.empty:
    table = age_distribution.reset_index()
    table.columns = ['年齡組', '病患數量']
    table['百分比'] = (table['病患數量'] / table['病患數量'].sum() * 100).round(2)
else:
    table = pd.DataFrame()
'''
        
        return code
    
    def _generate_comparison_code(self, question: str, outputs: List[OutputType], privacy_level: PrivacyLevel) -> str:
        """生成比較分析程式碼"""
        
        code = f'''# 生成程式碼: {question}
# 隱私等級: {privacy_level}
# 輸出類型: {', '.join(outputs)}

import pandas as pd
import matplotlib.pyplot as plt

# 讀取 Excel 資料
df = pd.read_excel('{settings.dataset_path}/patients.xlsx')

# 性別比較
gender_comparison = df['gender'].value_counts()

# 教育程度比較
education_comparison = df['education_years'].value_counts().sort_index()

# 隱私保護
if "{privacy_level.value}" == "k_anonymous":
    if len(df) < {settings.k_anonymity}:
        gender_comparison = pd.Series()
        education_comparison = pd.Series()
    else:
        # 確保每個組別都有足夠的樣本
        gender_comparison = gender_comparison[gender_comparison >= {settings.k_anonymity}]
        education_comparison = education_comparison[education_comparison >= {settings.k_anonymity}]

# 生成輸出
'''
        
        if OutputType.PLOT in outputs:
            code += '''
# 生成比較圖
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# 性別比較
if not gender_comparison.empty:
    gender_comparison.plot(kind='pie', ax=ax1, autopct='%1.1f%%')
    ax1.set_title('性別分布', fontsize=14, fontweight='bold')
    ax1.set_ylabel('')

# 教育程度比較
if not education_comparison.empty:
    education_comparison.plot(kind='bar', ax=ax2)
    ax2.set_title('教育程度分布', fontsize=14, fontweight='bold')
    ax2.set_xlabel('教育年數')
    ax2.set_ylabel('病患數量')
    ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('/artifacts/comparison_charts.png', dpi=300, bbox_inches='tight')
plot = plt.gcf()
'''
        
        if OutputType.TABLE in outputs:
            code += '''
# 生成比較表格
comparison_data = []
if not gender_comparison.empty:
    for gender, count in gender_comparison.items():
        comparison_data.append(['性別', gender, count, f"{(count/len(df)*100):.1f}%"])

if not education_comparison.empty:
    for edu, count in education_comparison.items():
        comparison_data.append(['教育年數', str(edu), count, f"{(count/len(df)*100):.1f}%"])

table = pd.DataFrame(comparison_data, columns=['類別', '分組', '數量', '百分比'])
'''
        
        return code
    
    def _generate_general_analysis_code(self, question: str, outputs: List[OutputType], privacy_level: PrivacyLevel) -> str:
        """生成一般分析程式碼"""
        
        code = f'''# 生成程式碼: {question}
# 隱私等級: {privacy_level}
# 輸出類型: {', '.join(outputs)}

import pandas as pd
import matplotlib.pyplot as plt

# 讀取 Excel 資料
df = pd.read_excel('{settings.dataset_path}/patients.xlsx')

# 基本資料概覽
print(f"資料集大小: {{df.shape}}")
print(f"欄位: {{list(df.columns)}}")

# 基本統計
summary_stats = df.describe()

# 隱私保護
if "{privacy_level.value}" == "k_anonymous":
    if len(df) < {settings.k_anonymity}:
        summary_stats = pd.DataFrame()
    else:
        # 聚合資料以確保隱私
        summary_stats = df.agg(['count', 'mean', 'std']).round(2)

# 生成輸出
'''
        
        if OutputType.TABLE in outputs:
            code += '''
# 生成統計表格
if not summary_stats.empty:
    table = summary_stats.T
    table = table.reset_index()
    table.columns = ['欄位', '數量', '平均值', '標準差']
else:
    table = pd.DataFrame()
'''
        
        if OutputType.EXPLANATION in outputs:
            code += '''
# 生成分析說明
if not summary_stats.empty:
    explanation = f"資料集包含 {{len(df)}} 筆記錄，{len(df.columns)} 個欄位。"
    explanation += "主要數值欄位的統計資訊已整理成表格。"
else:
    explanation = "由於隱私保護要求，無法顯示詳細的統計資訊。"
'''
        
        return code
