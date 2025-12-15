#!/usr/bin/env python3
"""
使用 AI Builders 部署 API 部署网站
"""

import os
import json
import requests
from dotenv import load_dotenv
import subprocess
import sys

load_dotenv()

def get_git_repo_url():
    """获取 git 仓库 URL"""
    try:
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except:
        return None

def deploy():
    """部署到 AI Builders"""
    
    # 获取 API token
    api_token = os.getenv("AI_BUILDER_TOKEN")
    if not api_token:
        print("❌ 错误: 未找到 AI_BUILDER_TOKEN")
        print("请确保 .env 文件中有 AI_BUILDER_TOKEN")
        sys.exit(1)
    
    # 获取仓库 URL
    repo_url = get_git_repo_url()
    if not repo_url:
        print("❌ 错误: 未找到 git 远程仓库")
        print("请先添加 git remote:")
        print("  git remote add origin https://github.com/your-username/your-repo.git")
        sys.exit(1)
    
    # 部署参数
    service_name = input("请输入服务名称 (默认: ai-usage-analytics): ").strip() or "ai-usage-analytics"
    branch = input("请输入分支名称 (默认: main): ").strip() or "main"
    port = int(input("请输入端口 (默认: 8000): ").strip() or "8000")
    
    print(f"\n部署配置:")
    print(f"  仓库 URL: {repo_url}")
    print(f"  服务名称: {service_name}")
    print(f"  分支: {branch}")
    print(f"  端口: {port}")
    
    confirm = input("\n确认部署? (y/n): ").strip().lower()
    if confirm != 'y':
        print("取消部署")
        sys.exit(0)
    
    # 调用部署 API
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
    
    print(f"\n正在部署到 AI Builders...")
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        print(f"\n✅ 部署请求已提交!")
        print(f"\n部署信息:")
        print(f"  服务名称: {result.get('service_name', service_name)}")
        print(f"  状态: {result.get('status', 'queued')}")
        print(f"  消息: {result.get('message', '')}")
        
        if result.get('public_url'):
            print(f"\n🌐 部署完成后访问:")
            print(f"  {result.get('public_url')}")
        else:
            print(f"\n🌐 部署完成后访问:")
            print(f"  https://{service_name}.ai-builders.space")
        
        print(f"\n⏳ 请等待 5-10 分钟完成部署")
        print(f"   可以查看部署状态或等待完成通知")
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 部署失败: {e}")
        if hasattr(e, 'response') and e.response:
            try:
                error_data = e.response.json()
                print(f"错误详情: {error_data}")
            except:
                print(f"响应: {e.response.text}")
        sys.exit(1)

if __name__ == "__main__":
    deploy()

