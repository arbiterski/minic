#!/usr/bin/env python3
"""
安裝必要的 Python 套件
"""

import subprocess
import sys

def install_package(package):
    """安裝套件"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} 安裝成功")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ {package} 安裝失敗")
        return False

def main():
    """主函數"""
    print("📦 安裝阿茲海默症分析資料庫依賴套件")
    print("=" * 50)
    
    # 必要的套件
    packages = [
        "pandas",
        "matplotlib", 
        "numpy",
        "openpyxl",
        "requests",
        "flask"
    ]
    
    print("正在安裝套件...")
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 安裝結果: {success_count}/{len(packages)} 成功")
    
    if success_count == len(packages):
        print("🎉 所有套件安裝成功！")
        print("🚀 現在可以運行 app_simple.py 了")
    else:
        print("⚠️  部分套件安裝失敗，請手動安裝")
        print("💡 建議使用: pip install pandas matplotlib numpy openpyxl requests")

if __name__ == "__main__":
    main()
