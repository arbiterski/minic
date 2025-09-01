#!/usr/bin/env python3
"""
測試 Claude Code Server 整合的腳本
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.claude_code_server import ClaudeCodeServer
from app.models.schemas import OutputType, PrivacyLevel

def test_claude_code_server():
    """測試 Claude Code Server 整合"""
    
    print("🧪 測試 Claude Code Server 整合")
    print("=" * 50)
    
    # 創建服務實例
    claude_service = ClaudeCodeServer()
    
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
            # 生成程式碼
            result = claude_service.generate_code(
                question=question,
                outputs=[OutputType.PLOT, OutputType.TABLE, OutputType.EXPLANATION],
                privacy_level=PrivacyLevel.K_ANONYMOUS
            )
            
            print(f"✅ 程式碼生成成功")
            print(f"   來源: {result.get('source', 'unknown')}")
            print(f"   程式碼雜湊: {result['code_hash'][:16]}...")
            print(f"   語言: {result['language']}")
            print(f"   使用庫: {', '.join(result['libraries'])}")
            
            # 顯示程式碼前幾行
            code_lines = result['code'].split('\n')[:10]
            print(f"   程式碼預覽:")
            for line in code_lines:
                if line.strip():
                    print(f"     {line}")
            if len(result['code'].split('\n')) > 10:
                print(f"     ... (共 {len(result['code'].split('\n'))} 行)")
                
        except Exception as e:
            print(f"❌ 程式碼生成失敗: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 測試完成！")

if __name__ == "__main__":
    test_claude_code_server()
