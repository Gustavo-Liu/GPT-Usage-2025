#!/usr/bin/env python3
"""
立即部署到 AI Builders
"""

import requests
import json
import sys

API_TOKEN = "sk_612ffd16_2f4afacbc641f99b6122dc696e4715dfc2b3"
REPO_URL = "https://github.com/Gustavo-Liu/GPT-Usage-2025.git"
SERVICE_NAME = "ai-usage-analytics"
BRANCH = "main"
PORT = 8000

def main():
    print("=" * 60)
    print("🚀 开始部署 AI 使用习惯分析网站")
    print("=" * 60)
    print(f"\n📋 部署配置:")
    print(f"   仓库: {REPO_URL}")
    print(f"   服务名称: {SERVICE_NAME}")
    print(f"   分支: {BRANCH}")
    print(f"   端口: {PORT}\n")

    api_url = "https://space.ai-builders.com/backend/v1/deployments"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "repo_url": REPO_URL,
        "service_name": SERVICE_NAME,
        "branch": BRANCH,
        "port": PORT
    }

    try:
        print("⏳ 正在提交部署请求到 AI Builders...")
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        print(f"\n📡 HTTP 状态码: {response.status_code}")
        
        if response.status_code == 202:
            result = response.json()
            print("\n" + "=" * 60)
            print("✅ 部署请求已成功提交!")
            print("=" * 60)
            print("\n📦 部署信息:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            public_url = result.get('public_url') or f"https://{SERVICE_NAME}.ai-builders.space"
            print(f"\n🌐 部署完成后访问:")
            print(f"   {public_url}")
            print(f"\n⏰ 预计等待时间: 5-10 分钟")
            print(f"   请稍后访问上述链接查看部署状态")
            print("\n💡 提示: 可以使用以下命令查看部署状态:")
            print(f"   curl https://space.ai-builders.com/backend/v1/deployments/{SERVICE_NAME}")
            
            return 0
            
        else:
            print("\n" + "=" * 60)
            print(f"❌ 部署失败 (状态码: {response.status_code})")
            print("=" * 60)
            try:
                error_data = response.json()
                print("\n错误详情:")
                print(json.dumps(error_data, indent=2, ensure_ascii=False))
            except:
                print(f"\n响应内容:\n{response.text}")
            return 1
            
    except requests.exceptions.RequestException as e:
        print("\n" + "=" * 60)
        print(f"❌ 网络请求错误: {e}")
        print("=" * 60)
        return 1
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ 发生错误: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

