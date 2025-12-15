#!/usr/bin/env python3
"""
快速部署脚本 - 使用提供的 API token
"""

import requests
import json
import sys

# 使用你提供的 API token
API_TOKEN = "sk_612ffd16_2f4afacbc641f99b6122dc696e4715dfc2b3"

def deploy():
    """部署到 AI Builders"""
    
    print("🚀 AI 使用习惯分析网站部署")
    print("=" * 50)
    
    # 获取输入
    repo_url = input("\n请输入 GitHub 仓库 URL: ").strip()
    if not repo_url:
        print("❌ 错误: 需要提供仓库 URL")
        sys.exit(1)
    
    service_name = input("请输入服务名称 (默认: ai-usage-analytics): ").strip() or "ai-usage-analytics"
    branch = input("请输入分支 (默认: main): ").strip() or "main"
    port = int(input("请输入端口 (默认: 8000): ").strip() or "8000")
    
    print(f"\n📋 部署配置:")
    print(f"  仓库 URL: {repo_url}")
    print(f"  服务名称: {service_name}")
    print(f"  分支: {branch}")
    print(f"  端口: {port}")
    
    confirm = input("\n确认部署? (y/n): ").strip().lower()
    if confirm != 'y':
        print("取消部署")
        sys.exit(0)
    
    # API 请求
    api_url = "https://space.ai-builders.com/backend/v1/deployments"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "repo_url": repo_url,
        "service_name": service_name,
        "branch": branch,
        "port": port
    }
    
    print(f"\n⏳ 正在部署...")
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        print(f"\n📡 响应状态: {response.status_code}")
        
        if response.status_code == 202:
            result = response.json()
            print(f"\n✅ 部署请求已成功提交!")
            print(f"\n📦 部署信息:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            if result.get('public_url'):
                print(f"\n🌐 部署完成后访问:")
                print(f"   {result.get('public_url')}")
            else:
                print(f"\n🌐 部署完成后访问:")
                print(f"   https://{service_name}.ai-builders.space")
            
            print(f"\n⏰ 预计等待时间: 5-10 分钟")
            print(f"   可以稍后访问上述链接查看部署状态")
            
        else:
            print(f"\n❌ 部署失败")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2, ensure_ascii=False))
            except:
                print(f"响应内容: {response.text}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 请求失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    deploy()

