#!/bin/bash

# 阿茲海默症分析資料庫 - 簡化啟動腳本

echo "🧠 阿茲海默症分析資料庫 - 簡化版本"
echo "=================================="

# 檢查 Python 版本
echo "🐍 檢查 Python 環境..."
if command -v python3 > /dev/null 2>&1; then
    python_version=$(python3 --version)
    echo "  ✅ Python: $python_version"
else
    echo "  ❌ Python3 未找到，請先安裝 Python 3.7+"
    exit 1
fi

# 檢查資料檔案
echo ""
echo "📁 檢查資料檔案..."
excel_file="data/alzheimers_cohort_v1/patients.xlsx"
if [ -f "$excel_file" ]; then
    echo "  ✅ 找到 Excel 檔案: $excel_file"
else
    echo "  ❌ 找不到 Excel 檔案: $excel_file"
    echo "     請確保檔案已放置在正確位置"
    exit 1
fi

# 檢查 Claude Code Server
echo ""
echo "🤖 檢查 Claude Code Server..."
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "  ✅ Claude Code Server 正在運行 (localhost:3000)"
else
    echo "  ⚠️  Claude Code Server 未運行 (localhost:3000)"
    echo "     將使用預設程式碼生成"
fi

# 安裝依賴
echo ""
echo "📦 檢查依賴套件..."
if python3 -c "import pandas, matplotlib, numpy, openpyxl, requests" 2>/dev/null; then
    echo "  ✅ 所有依賴套件已安裝"
else
    echo "  ⚠️  缺少依賴套件，正在安裝..."
    python3 install_deps.py
fi

# 創建 artifacts 目錄
echo ""
echo "📁 創建輸出目錄..."
mkdir -p artifacts
echo "  ✅ 輸出目錄已準備就緒"

# 啟動應用
echo ""
echo "🚀 啟動分析資料庫..."
echo "=================================="
python3 app_simple.py

echo ""
echo "🎯 分析完成！"
echo "📁 結果檔案保存在: artifacts/ 目錄"
