#!/usr/bin/env python3
"""
修复部署：推送代码到 GitHub 并重新部署
"""

import subprocess
import sys
import time
import requests
import json
import os

REPO_URL = "https://github.com/Gustavo-Liu/GPT-Usage-2025.git"
API_TOKEN = "sk_612ffd16_2f4afacbc641f99b6122dc696e4715dfc2b3"
SERVICE_NAME = "ai-usage-analytics"

def run_cmd(cmd, check=True):
    """运行命令"""
    print(f"执行: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        if result.stdout:
            print(result.stdout)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"错误: {e.stderr}")
        return False

def main():
    print("=" * 60)
    print("🔧 修复部署：推送代码并重新部署")
    print("=" * 60)
    
    os.chdir("/Users/liuyingte/Json Explore")
    
    # 1. 初始化 git（如果需要）
    if not os.path.exists(".git"):
        print("\n1️⃣ 初始化 git 仓库...")
        run_cmd("git init")
    
    # 2. 添加文件
    print("\n2️⃣ 添加文件...")
    run_cmd("git add app.py Dockerfile requirements.txt index.html styles.css app.js website_metrics.json detailed_explanations.json .gitignore", check=False)
    run_cmd("git add -A", check=False)
    
    # 3. 提交
    print("\n3️⃣ 提交更改...")
    run_cmd("git commit -m 'Add AI Usage Analytics Dashboard'", check=False)
    
    # 4. 设置远程
    print("\n4️⃣ 设置远程仓库...")
    run_cmd("git remote remove origin", check=False)
    run_cmd("git remote add origin https://github.com/Gustavo-Liu/GPT-Usage-2025.git")
    
    # 5. 设置分支
    print("\n5️⃣ 设置主分支...")
    run_cmd("git branch -M main", check=False)
    
    # 6. 推送
    print("\n6️⃣ 推送到 GitHub...")
    success = run_cmd("git push -u origin main", check=False)
    
    if not success:
        print("\n⚠️  推送可能需要 GitHub 认证")
        print("请手动执行:")
        print("  cd /Users/liuyingte/Json Explore")
        print("  git push -u origin main")
        print("\n或者使用 GitHub CLI:")
        print("  gh auth login")
        print("  git push -u origin main")
        return 1
    
    print("\n✅ 代码已推送到 GitHub!")
    
    # 7. 等待几秒
    print("\n⏳ 等待 5 秒让 GitHub 同步...")
    time.sleep(5)
    
    # 8. 部署
    print("\n7️⃣ 开始部署...")
    print("=" * 60)
    
    api_url = "https://space.ai-builders.com/backend/v1/deployments"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "repo_url": REPO_URL,
        "service_name": SERVICE_NAME,
        "branch": "main",
        "port": 8000
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        print(f"HTTP 状态码: {response.status_code}\n")
        
        if response.status_code == 202:
            result = response.json()
            print("✅ 部署请求已成功提交!\n")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            public_url = result.get('public_url') or f"https://{SERVICE_NAME}.ai-builders.space"
            print(f"\n🌐 部署完成后访问:")
            print(f"   {public_url}")
            print(f"\n⏰ 预计等待时间: 5-10 分钟")
            
        else:
            print(f"❌ 部署失败 (状态码: {response.status_code})")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2, ensure_ascii=False))
            except:
                print(f"响应: {response.text}")
            return 1
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

