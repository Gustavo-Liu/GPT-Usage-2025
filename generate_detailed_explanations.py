#!/usr/bin/env python3
"""
使用 AI 生成详细的指标说明和解释
"""

import pandas as pd
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from collections import Counter
import re

load_dotenv()

# 初始化客户端
API_BASE_URL = "https://space.ai-builders.com/backend/v1"
api_key = os.getenv("AI_BUILDER_TOKEN")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=api_key
)

# 读取数据
messages_df = pd.read_csv('messages.csv')
with open('website_metrics.json', 'r') as f:
    metrics = json.load(f)
with open('conversation_summaries_and_trends.md', 'r', encoding='utf-8') as f:
    summary_content = f.read()

def analyze_conversation_keywords():
    """分析对话标题提取关键词"""
    titles = messages_df['conversation_title'].dropna().tolist()
    
    # 技术相关关键词
    tech_keywords = []
    business_keywords = []
    creative_keywords = []
    learning_keywords = []
    
    tech_patterns = ['r ', 'python', 'sql', 'code', 'model', 'statistic', 'data', 'analysis', 'shiny', 'regression', 'glmm', 'gam']
    business_patterns = ['ppt', 'email', 'report', 'presentation', 'meeting', 'summary', '周报', '邮件']
    creative_patterns = ['3d', 'design', 'logo', 'image', 'photo', 'print', 'style', '生成', '设计']
    learning_patterns = ['explain', 'what is', 'how', 'concept', 'definition', '学习', '解释']
    
    for title in titles:
        title_lower = str(title).lower()
        if any(p in title_lower for p in tech_patterns):
            tech_keywords.append(title)
        if any(p in title_lower for p in business_patterns):
            business_keywords.append(title)
        if any(p in title_lower for p in creative_patterns):
            creative_keywords.append(title)
        if any(p in title_lower for p in learning_patterns):
            learning_keywords.append(title)
    
    return {
        'technical': list(set(tech_keywords))[:10],
        'business': list(set(business_keywords))[:10],
        'creative': list(set(creative_keywords))[:10],
        'learning': list(set(learning_keywords))[:10]
    }

def analyze_tool_usage():
    """分析工具使用情况"""
    tool_messages = messages_df[messages_df['role'] == 'tool']
    
    # 从 metadata 或 content_type 分析工具类型
    tool_types = []
    for _, msg in tool_messages.iterrows():
        if pd.notna(msg.get('content_type')):
            tool_types.append(str(msg['content_type']))
    
    tool_counter = Counter(tool_types)
    return dict(tool_counter.most_common(10))

def analyze_interaction_patterns():
    """分析交互模式的具体内容"""
    # 分析协作型、指导型、问答型的具体表现
    # 通过对话长度和消息类型来判断
    conv_stats = []
    
    for conv_id in messages_df['conversation_id'].unique()[:100]:  # 采样分析
        conv_msgs = messages_df[messages_df['conversation_id'] == conv_id]
        user_msgs = conv_msgs[conv_msgs['role'] == 'user']
        assistant_msgs = conv_msgs[conv_msgs['role'] == 'assistant']
        
        if len(user_msgs) > 0:
            # 分析用户消息特征
            avg_user_msg_length = user_msgs['text'].str.len().mean() if len(user_msgs) > 0 else 0
            has_code = conv_msgs['has_code'].any()
            has_tool = (conv_msgs['role'] == 'tool').any()
            
            conv_stats.append({
                'conv_id': conv_id,
                'length': len(conv_msgs),
                'user_count': len(user_msgs),
                'avg_user_length': avg_user_msg_length,
                'has_code': has_code,
                'has_tool': has_tool
            })
    
    return conv_stats

def call_ai_for_explanations(context_data):
    """调用 AI 生成详细解释"""
    
    prompt = f"""基于以下 AI 使用习惯分析数据，请为每个指标和可视化生成详细的解释说明。

数据概览：
- 总对话数: 800
- 总消息数: 13,146
- 使用天数: 300
- 工具使用率: 43.4%
- 技术深度指数: 26.6

对话类型分布：
- 深度技术咨询: 57.9%
- 商务文档优化: 6.9%
- 创意设计协作: 16.1%
- 专业知识学习: 15.0%
- 日常实用咨询: 5.0%

技术能力：
- 代码对话: 20.0% (R, Python, SQL)
- 图片对话: 14.8%
- 工具使用对话: 43.4%
- 多模态对话: 16.1%

交互模式：
- 协作型: 40%
- 指导型: 35%
- 问答型: 25%

活跃时段：
- 最活跃: 18:00 (1608条消息)
- 最不活跃: 11:00 (26条消息)

个性化指标：
- 技术深度指数: 26.6
- 创意探索指数: 30.9
- 工作流整合度: 92.2

关键词分析：
{json.dumps(context_data['keywords'], ensure_ascii=False, indent=2)}

工具使用分析：
{json.dumps(context_data['tool_usage'], ensure_ascii=False, indent=2)}

请按照以下要求生成详细说明：

1. **对话类型分布的关键词说明**：
   为每个类型列出 3-5 个具体的关键词示例（如"创意设计协作：3D模型创造、Logo设计、图像生成、风格转换"）

2. **技术能力使用的详细说明**：
   - 编程语言的具体使用场景（R用于什么、Python用于什么）
   - 使用的具体工具（搜索工具用于什么、图像生成工具用于什么）
   - 多模态的具体应用场景

3. **活跃时间段趋势分析**（3-5句话）：
   分析使用时间模式，包括工作日vs周末、白天vs晚上等

4. **交互模式分布的具体说明**：
   - 协作型：协作什么？给出频率前三的类别
   - 指导型：指导什么？给出频率前三的类别
   - 问答型：问答什么？给出频率前三的类别

5. **雷达图各项目的解释和算法**：
   为每个维度（技术深度、创意探索、工作流整合、迭代优化、多模态使用、工具使用）提供：
   - 解释（这个指标代表什么）
   - 算法（如何计算的，公式或逻辑）

6. **身份定位的副业身份**：
   基于数据分析（医疗统计、3D打印、摄影、音乐等兴趣），推测副业身份

7. **AI关系定位的详细说明**：
   - 技术导师：教导了什么技术？具体示例
   - 创意伙伴：提供了什么创意？具体示例
   - 效率工具：在哪些方面提高了效率？具体场景（协作、代码、探索兴趣点等）

请用 JSON 格式返回结果，格式如下：
{{
    "conversation_types_details": {{
        "technical": {{"keywords": ["关键词1", "关键词2"], "description": "说明"}},
        "business": {{"keywords": [...], "description": "说明"}},
        "creative": {{"keywords": [...], "description": "说明"}},
        "learning": {{"keywords": [...], "description": "说明"}},
        "daily": {{"keywords": [...], "description": "说明"}}
    }},
    "technical_details": {{
        "languages": {{
            "R": "使用场景说明",
            "Python": "使用场景说明",
            "SQL": "使用场景说明"
        }},
        "tools": {{
            "搜索工具": "使用场景说明",
            "图像生成": "使用场景说明",
            "文件处理": "使用场景说明"
        }},
        "modalities": {{
            "多模态": "具体应用场景说明"
        }}
    }},
    "time_analysis": "3-5句话的趋势分析",
    "interaction_details": {{
        "collaborative": {{
            "description": "协作什么",
            "top3_categories": ["类别1", "类别2", "类别3"]
        }},
        "guidance": {{
            "description": "指导什么",
            "top3_categories": ["类别1", "类别2", "类别3"]
        }},
        "qa": {{
            "description": "问答什么",
            "top3_categories": ["类别1", "类别2", "类别3"]
        }}
    }},
    "radar_explanations": {{
        "tech_depth": {{
            "interpretation": "解释",
            "algorithm": "算法/公式"
        }},
        "creative_exploration": {{...}},
        "workflow_integration": {{...}},
        "iterative_optimization": {{...}},
        "multimodal_usage": {{...}},
        "tool_usage": {{...}}
    }},
    "identity": {{
        "main": "主身份",
        "side": "副业身份"
    }},
    "ai_relationship": {{
        "technical_mentor": {{
            "description": "教导了什么技术",
            "examples": ["示例1", "示例2"]
        }},
        "creative_partner": {{
            "description": "提供了什么创意",
            "examples": ["示例1", "示例2"]
        }},
        "efficiency_tool": {{
            "description": "在哪些方面提高效率",
            "scenarios": ["场景1", "场景2", "场景3"]
        }}
    }}
}}"""

    try:
        response = client.chat.completions.create(
            model="gemini-2.5-pro",
            messages=[
                {"role": "system", "content": "你是一个专业的数据分析专家，擅长从数据中提取洞察并生成清晰、具体的解释说明。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        result_text = response.choices[0].message.content
        
        # 尝试提取 JSON
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            # 如果没有 JSON，返回原始文本
            return {"raw": result_text}
            
    except Exception as e:
        print(f"AI 调用错误: {e}")
        return None

def main():
    print("正在分析数据...")
    
    # 分析关键词
    keywords = analyze_conversation_keywords()
    
    # 分析工具使用
    tool_usage = analyze_tool_usage()
    
    context_data = {
        'keywords': keywords,
        'tool_usage': tool_usage
    }
    
    print("正在调用 AI 生成详细解释...")
    explanations = call_ai_for_explanations(context_data)
    
    if explanations:
        output_file = 'detailed_explanations.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(explanations, f, indent=2, ensure_ascii=False)
        print(f"✅ 详细解释已保存到: {output_file}")
    else:
        print("❌ 生成失败")

if __name__ == "__main__":
    main()

