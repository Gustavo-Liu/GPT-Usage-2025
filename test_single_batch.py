#!/usr/bin/env python3
"""
测试版本：只处理第一个批次的对话（30个对话）
"""

import pandas as pd
import json
import os
from datetime import datetime
from typing import List
from openai import OpenAI
from dotenv import load_dotenv


# 加载环境变量
load_dotenv()

# 初始化 OpenAI 客户端
API_BASE_URL = "https://space.ai-builders.com/backend/v1"
api_key = os.getenv("AI_BUILDER_TOKEN")

if not api_key:
    raise ValueError("未找到 AI_BUILDER_TOKEN，请检查 .env 文件")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=api_key
)


def prepare_conversation_summary(messages_df: pd.DataFrame, conv_id: str) -> str:
    """为单个对话准备摘要文本"""
    conv_messages = messages_df[messages_df['conversation_id'] == conv_id].copy()
    
    if len(conv_messages) == 0:
        return ""
    
    title = conv_messages.iloc[0]['conversation_title'] or "无标题"
    conv_messages = conv_messages.sort_values('create_time')
    
    summary_parts = [f"对话标题: {title}\n对话ID: {conv_id}\n\n"]
    
    for idx, msg in conv_messages.iterrows():
        role = msg['role']
        if pd.isna(role):
            continue
            
        text = str(msg['text']) if pd.notna(msg['text']) else ""
        if len(text.strip()) < 10:
            continue
        
        # 截断过长的文本
        if len(text) > 500:
            text = text[:500] + "...[已截断]"
        
        # 添加标签
        tags = []
        if msg['has_code']:
            tags.append("代码")
        if msg['has_image']:
            tags.append("图片")
        if msg['has_link']:
            tags.append("链接")
        tag_str = f"[{', '.join(tags)}]" if tags else ""
        
        summary_parts.append(f"{role.upper()}: {text} {tag_str}\n")
    
    return "\n".join(summary_parts)


def generate_batch_summaries(conversations_text: List[str]) -> str:
    """调用 API 为一批对话生成总结"""
    conversations_combined = "\n\n" + "="*80 + "\n\n".join(
        f"【对话 {i+1}】\n{conv}" 
        for i, conv in enumerate(conversations_text)
    )
    
    prompt = f"""你是一个专业的对话分析专家。下面是 {len(conversations_text)} 个用户与 AI 的对话记录。

请为每个对话生成一个简洁的总结（2-3句话），重点关注：
1. 对话的主要话题和目的
2. 用户的主要需求和问题
3. AI 提供的帮助类型（编程、文本生成、问题解答等）
4. 对话的特点（是否涉及代码、图片、工具使用等）

对话记录：
{conversations_combined}

请按照以下格式输出每个对话的总结：
【对话 1】
总结：[2-3句话的总结]

【对话 2】
总结：[2-3句话的总结]

...（依此类推）

保持总结简洁但信息丰富，能够体现用户的 AI 使用习惯和偏好。"""

    print(f"正在调用 API 生成总结（{len(conversations_text)} 个对话）...")
    
    try:
        response = client.chat.completions.create(
            model="deepseek",
            messages=[
                {"role": "system", "content": "你是一个专业的对话分析专家，擅长从对话中提取关键信息和用户行为模式。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        summary = response.choices[0].message.content
        return summary
        
    except Exception as e:
        print(f"⚠️ API 调用出错: {e}")
        import traceback
        traceback.print_exc()
        return f"[生成失败: {str(e)}]"


def main():
    """主函数 - 只处理第一个批次"""
    print("="*80)
    print("测试版本：处理第一个批次（30个对话）")
    print("="*80)
    
    messages_file = "messages.csv"
    batch_size = 30
    output_file = "test_batch_summary.md"
    
    # 读取数据
    print(f"\n正在读取 {messages_file}...")
    messages_df = pd.read_csv(messages_file)
    print(f"总消息数: {len(messages_df)}")
    
    # 获取前30个对话 ID
    conversation_ids = messages_df['conversation_id'].unique().tolist()[:batch_size]
    print(f"本次测试处理对话数: {len(conversation_ids)}")
    
    # 准备对话摘要
    print(f"\n正在准备对话摘要...")
    batch_texts = []
    
    for i, conv_id in enumerate(conversation_ids, 1):
        conv_text = prepare_conversation_summary(messages_df, conv_id)
        if conv_text:
            batch_texts.append(conv_text)
            if i % 10 == 0:
                print(f"  已准备 {i}/{len(conversation_ids)} 个对话")
    
    print(f"  准备完成，有效对话数: {len(batch_texts)}")
    
    # 调用 API 生成总结
    print(f"\n正在生成总结...")
    batch_summary = generate_batch_summaries(batch_texts)
    
    # 保存结果
    print(f"\n正在保存结果到: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 测试批次对话总结\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"处理对话数: {len(batch_texts)}\n\n")
        f.write("="*80 + "\n\n")
        f.write(batch_summary)
        f.write("\n")
    
    print(f"\n✅ 完成！结果已保存到: {output_file}")
    print(f"\n总结预览:")
    print("-" * 80)
    # 显示前500个字符
    preview = batch_summary[:500] + "..." if len(batch_summary) > 500 else batch_summary
    print(preview)
    print("-" * 80)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

