#!/usr/bin/env python3
"""
安全的部署脚本 - 使用环境变量中的 API token
"""

import os
import json
import requests
from dotenv import load_dotenv
import sys

load_dotenv()

def deploy():
    """部署到 AI Builders"""
    
    # 从环境变量获取 API token
    api_token = os.getenv("AI_BUILDER_TOKEN")
    if not api_token:
        print("❌ 错误: 未找到 AI_BUILDER_TOKEN 环境变量")
        print("请在 .env 文件中设置 AI_BUILDER_TOKEN")
        sys.exit(1)
    
    # 配置
    repo_url = "https://github.com/Gustavo-Liu/GPT-Usage-2025.git"
    service_name = "ai-usage-analytics"
    branch = "main"
    port = 8000
    
    print("=" * 60)
    print("🚀 部署 AI 使用习惯分析网站")
    print("=" * 60)
    print(f"\n📋 部署配置:")
    print(f"   仓库: {repo_url}")
    print(f"   服务名称: {service_name}")
    print(f"   分支: {branch}")
    print(f"   端口: {port}\n")
    
    # API 请求
    api_url = "https://space.ai-builders.com/backend/v1/deployments"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "repo_url": repo_url,
        "service_name": service_name,
        "branch": branch,
        "port": port
    }
    
    try:
        print("⏳ 正在提交部署请求...")
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        print(f"\n📡 HTTP 状态码: {response.status_code}")
        
        if response.status_code == 202:
            result = response.json()
            print("\n✅ 部署请求已成功提交!\n")
            print("📦 部署信息:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            public_url = result.get('public_url') or f"https://{service_name}.ai-builders.space"
            print(f"\n🌐 部署完成后访问:")
            print(f"   {public_url}")
            print(f"\n⏰ 预计等待时间: 5-10 分钟")
            
        else:
            print(f"\n❌ 部署失败 (状态码: {response.status_code})")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2, ensure_ascii=False))
            except:
                print(f"响应内容:\n{response.text}")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    deploy()
