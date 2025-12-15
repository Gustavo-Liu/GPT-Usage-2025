#!/usr/bin/env python3
"""
为每个对话生成总结，并分析整体趋势

功能：
1. 读取 messages.csv，按对话分组
2. 为每个对话构建摘要文本
3. 每 30 个对话打包，调用 deepseek API 生成总结
4. 最后分析所有对话的整体趋势和脉络
"""

import pandas as pd
import json
import os
import time
from datetime import datetime
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
import sys


# 加载环境变量
load_dotenv()

# 初始化 OpenAI 客户端（使用 AI Builders API）
API_BASE_URL = "https://space.ai-builders.com/backend/v1"
api_key = os.getenv("AI_BUILDER_TOKEN")

if not api_key:
    raise ValueError("未找到 AI_BUILDER_TOKEN，请检查 .env 文件")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=api_key
)


def prepare_conversation_summary(messages_df: pd.DataFrame, conv_id: str) -> str:
    """
    为单个对话准备摘要文本
    
    Args:
        messages_df: 消息 DataFrame
        conv_id: 对话 ID
        
    Returns:
        格式化的对话摘要文本
    """
    conv_messages = messages_df[messages_df['conversation_id'] == conv_id].copy()
    
    if len(conv_messages) == 0:
        return ""
    
    # 获取对话标题
    title = conv_messages.iloc[0]['conversation_title'] or "无标题"
    
    # 按时间排序
    conv_messages = conv_messages.sort_values('create_time')
    
    # 提取主要消息（用户和助手）
    summary_parts = [f"对话标题: {title}\n对话ID: {conv_id}\n\n"]
    
    for idx, msg in conv_messages.iterrows():
        role = msg['role']
        if pd.isna(role):
            continue
            
        text = str(msg['text']) if pd.notna(msg['text']) else ""
        content_type = str(msg['content_type']) if pd.notna(msg['content_type']) else ""
        
        # 只保留有意义的文本（长度大于 10）
        if len(text.strip()) < 10:
            continue
        
        # 截断过长的文本（保留前 500 字符）
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


def generate_batch_summaries(conversations_text: List[str], batch_num: int) -> str:
    """
    调用 API 为一批对话生成总结
    
    Args:
        conversations_text: 对话文本列表
        batch_num: 批次编号
        
    Returns:
        API 返回的总结文本
    """
    # 构建提示词
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

    print(f"  正在调用 API 生成批次 {batch_num} 的总结（{len(conversations_text)} 个对话）...")
    
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
        print(f"  ⚠️ API 调用出错: {e}")
        return f"[批次 {batch_num} 生成失败: {str(e)}]"


def analyze_overall_trends(all_summaries: List[str]) -> str:
    """
    分析所有对话的整体趋势和脉络
    
    Args:
        all_summaries: 所有对话的总结列表
        
    Returns:
        整体趋势分析文本
    """
    # 合并所有总结
    summaries_text = "\n\n".join(
        f"【对话总结 {i+1}】\n{summary}" 
        for i, summary in enumerate(all_summaries)
    )
    
    prompt = f"""基于以下 {len(all_summaries)} 个对话的总结，请分析这个用户的 AI 使用习惯和对话趋势。

对话总结：
{summaries_text}

请从以下维度进行深入分析：

1. **使用模式与偏好**
   - 用户最常使用 AI 做什么？（编程、文本生成、问题解答、学习等）
   - 对话的主要类型分布
   - 用户的使用习惯特点（深度探讨 vs 快速问答、单一话题 vs 多话题等）

2. **技术倾向**
   - 是否经常使用代码相关功能
   - 是否使用图片分析功能
   - 工具使用情况
   - 对 AI 功能的探索程度

3. **对话特点**
   - 对话的平均深度和复杂度
   - 用户的提问方式（详细 vs 简洁、具体 vs 抽象）
   - 与 AI 的交互模式（指导型、协作型、问答型等）

4. **时间趋势（如果可能）**
   - 使用习惯是否有变化
   - 话题偏好是否有演变

5. **个性化画像**
   - 用 3-5 句话总结这个用户的 AI 使用画像
   - 描述最突出的使用特点

请用清晰的结构输出，每个维度单独成段，最后给出一个综合性的用户画像。"""

    print("\n正在分析整体趋势和脉络...")
    
    try:
        response = client.chat.completions.create(
            model="deepseek",
            messages=[
                {"role": "system", "content": "你是一个专业的行为分析专家，擅长从大量数据中提取用户行为模式和趋势。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=4000
        )
        
        analysis = response.choices[0].message.content
        return analysis
        
    except Exception as e:
        print(f"⚠️ 整体趋势分析失败: {e}")
        return f"[整体趋势分析失败: {str(e)}]"


def main():
    """主函数"""
    print("="*80)
    print("对话总结生成工具")
    print("="*80)
    
    # 参数
    messages_file = "messages.csv"
    batch_size = 30
    output_file = "conversation_summaries_and_trends.md"
    
    # 读取数据
    print(f"\n正在读取 {messages_file}...")
    messages_df = pd.read_csv(messages_file)
    print(f"总消息数: {len(messages_df)}")
    
    # 获取所有对话 ID
    conversation_ids = messages_df['conversation_id'].unique().tolist()
    total_conversations = len(conversation_ids)
    print(f"总对话数: {total_conversations}")
    
    # 准备对话摘要
    print(f"\n正在准备对话摘要（批量大小: {batch_size}）...")
    conversation_summaries = []
    
    # 分批处理
    num_batches = (total_conversations + batch_size - 1) // batch_size
    
    for batch_idx in range(num_batches):
        start_idx = batch_idx * batch_size
        end_idx = min((batch_idx + 1) * batch_size, total_conversations)
        batch_ids = conversation_ids[start_idx:end_idx]
        
        print(f"\n处理批次 {batch_idx + 1}/{num_batches} (对话 {start_idx + 1}-{end_idx})")
        
        # 准备这批对话的文本
        batch_texts = []
        for conv_id in batch_ids:
            conv_text = prepare_conversation_summary(messages_df, conv_id)
            if conv_text:
                batch_texts.append(conv_text)
        
        if not batch_texts:
            print(f"  批次 {batch_idx + 1} 没有有效对话，跳过")
            continue
        
        # 调用 API 生成总结
        batch_summary = generate_batch_summaries(batch_texts, batch_idx + 1)
        conversation_summaries.append(batch_summary)
        
        # 避免 API 限流
        if batch_idx < num_batches - 1:
            print(f"  等待 2 秒...")
            time.sleep(2)
    
    print(f"\n共生成 {len(conversation_summaries)} 个批次的总结")
    
    # 分析整体趋势
    print("\n" + "="*80)
    overall_trends = analyze_overall_trends(conversation_summaries)
    
    # 生成最终报告
    print(f"\n正在生成最终报告: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# AI 对话总结与使用趋势分析\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"分析对话总数: {total_conversations}\n")
        f.write(f"批次数量: {len(conversation_summaries)}\n\n")
        
        f.write("="*80 + "\n\n")
        f.write("# 各批次对话总结\n\n")
        for i, summary in enumerate(conversation_summaries, 1):
            f.write(f"## 批次 {i}\n\n")
            f.write(summary)
            f.write("\n\n" + "-"*80 + "\n\n")
        
        f.write("="*80 + "\n\n")
        f.write("# 整体趋势与用户画像分析\n\n")
        f.write(overall_trends)
        f.write("\n")
    
    print(f"\n✅ 完成！报告已保存到: {output_file}")
    print(f"   总对话数: {total_conversations}")
    print(f"   生成批次: {len(conversation_summaries)}")
    print(f"   最终报告包含:")
    print(f"   - 所有对话的详细总结")
    print(f"   - 整体使用趋势和用户画像分析")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断，程序退出")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

