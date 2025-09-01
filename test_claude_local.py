#!/usr/bin/env python3
"""
本地測試 Claude Code Server 整合
"""

import requests
import json

def test_claude_code_server():
    """測試您的 Claude Code Server"""
    
    print("🧪 測試 Claude Code Server 整合")
    print("=" * 50)
    
    # 測試問題
    test_questions = [
        "歷年病患分布折線圖",
        "病患年齡分布統計",
        "性別與教育程度比較分析"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 測試問題 {i}: {question}")
        print("-" * 30)
        
        try:
            # 構建請求訊息
            message = f"""
請為以下阿茲海默症資料分析問題生成 Python 程式碼：

問題：{question}
隱私等級：k_anonymous
期望輸出：plot, table

要求：
1. 讀取 Excel 檔案：/data/alzheimers_cohort_v1/patients.xlsx
2. 生成 plot 和 table 輸出
3. 應用 k_anonymous 隱私保護
4. 使用 pandas, matplotlib, openpyxl 等庫
5. 將圖表保存到 /artifacts/ 目錄
6. 返回可執行的 Python 程式碼
            """.strip()
            
            # 發送請求到 Claude Code Server
            response = requests.post(
                "http://localhost:3000/api/execute",
                headers={"Content-Type": "application/json"},
                json={
                    "message": message,
                    "timeout": 30000
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Claude Code Server 回應成功")
                print(f"   狀態碼: {response.status_code}")
                
                # 顯示結果
                if 'result' in result:
                    code = result['result']
                    print(f"   程式碼長度: {len(code)} 字符")
                    print(f"   程式碼預覽:")
                    
                    # 顯示前幾行
                    code_lines = code.split('\n')[:10]
                    for line in code_lines:
                        if line.strip():
                            print(f"     {line}")
                    code_lines_count = len(code.split('\n'))
                    if code_lines_count > 10:
                        print(f"     ... (共 {code_lines_count} 行)")
                else:
                    print(f"   回應內容: {result}")
                    
            else:
                print(f"❌ Claude Code Server 回應錯誤")
                print(f"   狀態碼: {response.status_code}")
                print(f"   錯誤內容: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ 無法連接到 Claude Code Server (localhost:3000)")
            print(f"   請確保服務正在運行")
        except Exception as e:
            print(f"❌ 測試失敗: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 測試完成！")

if __name__ == "__main__":
    test_claude_code_server()
