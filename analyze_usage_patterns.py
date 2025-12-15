#!/usr/bin/env python3
"""
AI 使用习惯分析脚本
计算并可视化用户与 AI 交互的各种指标
"""

import pandas as pd
import json
import numpy as np
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体（如果需要）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def load_data(messages_file='messages.csv', edges_file='edges.csv'):
    """加载数据"""
    print("正在加载数据...")
    messages_df = pd.read_csv(messages_file)
    edges_df = pd.read_csv(edges_file)
    
    # 转换时间戳
    messages_df['datetime'] = pd.to_datetime(
        messages_df['create_time'], unit='s', errors='coerce'
    )
    messages_df['date'] = messages_df['datetime'].dt.date
    messages_df['hour'] = messages_df['datetime'].dt.hour
    messages_df['day_of_week'] = messages_df['datetime'].dt.day_name()
    
    # 计算子节点数量
    messages_df['children_count'] = messages_df['children_ids'].apply(
        lambda x: len(eval(x)) if pd.notna(x) and str(x) != '' and str(x) != 'nan' else 0
    )
    
    # 计算是否有分叉
    messages_df['has_branch'] = messages_df['children_count'] > 1
    
    return messages_df, edges_df


def calculate_metrics(messages_df, edges_df):
    """计算所有指标"""
    metrics = {}
    
    # 1. 基本统计
    metrics['total_conversations'] = messages_df['conversation_id'].nunique()
    metrics['total_messages'] = len(messages_df)
    metrics['total_edges'] = len(edges_df)
    metrics['date_span_days'] = (
        messages_df['datetime'].max() - messages_df['datetime'].min()
    ).days
    
    # 2. 对话长度统计
    conv_lengths = messages_df.groupby('conversation_id').size()
    metrics['avg_messages_per_conv'] = conv_lengths.mean()
    metrics['median_messages_per_conv'] = conv_lengths.median()
    metrics['max_messages_per_conv'] = conv_lengths.max()
    metrics['min_messages_per_conv'] = conv_lengths.min()
    
    # 3. 角色分布
    role_counts = messages_df['role'].value_counts()
    metrics['role_distribution'] = role_counts.to_dict()
    metrics['user_assistant_ratio'] = (
        role_counts.get('user', 0) / role_counts.get('assistant', 1)
    )
    
    # 4. 内容类型分布
    content_type_counts = messages_df['content_type'].value_counts()
    metrics['content_type_distribution'] = content_type_counts.to_dict()
    
    # 5. 内容标签统计
    metrics['messages_with_code'] = messages_df['has_code'].sum()
    metrics['messages_with_image'] = messages_df['has_image'].sum()
    metrics['messages_with_link'] = messages_df['has_link'].sum()
    metrics['code_percentage'] = (metrics['messages_with_code'] / len(messages_df)) * 100
    metrics['image_percentage'] = (metrics['messages_with_image'] / len(messages_df)) * 100
    metrics['link_percentage'] = (metrics['messages_with_link'] / len(messages_df)) * 100
    
    # 6. 分叉分析
    metrics['branching_nodes'] = messages_df['has_branch'].sum()
    metrics['branching_percentage'] = (metrics['branching_nodes'] / len(messages_df)) * 100
    metrics['max_children'] = messages_df['children_count'].max()
    metrics['avg_children'] = messages_df['children_count'].mean()
    
    # 7. 对话深度分析（简化版：计算每条对话的最大深度）
    def calculate_conversation_depth(conv_id, edges_df, messages_df):
        """计算单个对话的最大深度"""
        conv_edges = edges_df[edges_df['conversation_id'] == conv_id]
        conv_nodes = messages_df[messages_df['conversation_id'] == conv_id]
        
        # 找到根节点（parent_id 为 None 或不在 edges 中作为 child）
        root_nodes = conv_nodes[conv_nodes['parent_id'].isna()]['node_id'].tolist()
        if not root_nodes:
            # 如果没有明确的根，找没有 parent 边的节点
            parents_in_conv = set(conv_edges['parent_id'].unique())
            children_in_conv = set(conv_edges['child_id'].unique())
            root_candidates = parents_in_conv - children_in_conv
            root_nodes = list(root_candidates) if root_candidates else [conv_nodes.iloc[0]['node_id']]
        
        if not root_nodes:
            return 0
        
        # BFS 计算深度
        from collections import deque
        depths = {}
        queue = deque([(root_nodes[0], 0)])
        
        while queue:
            node, depth = queue.popleft()
            if node in depths:
                continue
            depths[node] = depth
            
            children = conv_edges[conv_edges['parent_id'] == node]['child_id'].tolist()
            for child in children:
                queue.append((child, depth + 1))
        
        return max(depths.values()) if depths else 0
    
    conv_ids = messages_df['conversation_id'].unique()
    depths = [calculate_conversation_depth(cid, edges_df, messages_df) for cid in conv_ids[:100]]  # 限制前100个以节省时间
    if depths:
        metrics['avg_conversation_depth'] = np.mean(depths)
        metrics['max_conversation_depth'] = max(depths)
        metrics['median_conversation_depth'] = np.median(depths)
    
    # 8. 时间分布
    metrics['daily_avg_conversations'] = (
        messages_df.groupby('date')['conversation_id'].nunique().mean()
    )
    metrics['daily_avg_messages'] = messages_df.groupby('date').size().mean()
    
    hour_counts = messages_df['hour'].value_counts().sort_index()
    metrics['most_active_hour'] = hour_counts.idxmax()
    metrics['least_active_hour'] = hour_counts.idxmin()
    
    # 9. Tool 使用
    tool_messages = messages_df[messages_df['role'] == 'tool']
    metrics['tool_usage_count'] = len(tool_messages)
    metrics['tool_usage_percentage'] = (len(tool_messages) / len(messages_df)) * 100
    
    # 10. 模型信息提取（从 metadata）
    model_slugs = []
    for meta_str in messages_df[messages_df['metadata_raw'].notna()]['metadata_raw']:
        try:
            meta = json.loads(meta_str)
            if 'model_slug' in meta:
                model_slugs.append(meta['model_slug'])
            elif 'default_model_slug' in meta:
                model_slugs.append(meta['default_model_slug'])
        except:
            pass
    
    if model_slugs:
        model_counts = Counter(model_slugs)
        metrics['model_distribution'] = dict(model_counts.most_common())
        metrics['most_used_model'] = model_counts.most_common(1)[0][0] if model_counts else None
    
    return metrics


def print_metrics_report(metrics):
    """打印指标报告"""
    print("\n" + "="*80)
    print("AI 使用习惯分析报告")
    print("="*80)
    
    print(f"\n【基本统计】")
    print(f"  总对话数: {metrics['total_conversations']}")
    print(f"  总消息数: {metrics['total_messages']}")
    print(f"  总边数: {metrics['total_edges']}")
    print(f"  使用时间跨度: {metrics['date_span_days']} 天")
    
    print(f"\n【对话长度】")
    print(f"  平均每条对话消息数: {metrics['avg_messages_per_conv']:.1f}")
    print(f"  中位数: {metrics['median_messages_per_conv']:.1f}")
    print(f"  最大: {metrics['max_messages_per_conv']}")
    print(f"  最小: {metrics['min_messages_per_conv']}")
    
    print(f"\n【角色分布】")
    for role, count in metrics['role_distribution'].items():
        print(f"  {role}: {count} ({count/metrics['total_messages']*100:.1f}%)")
    print(f"  User/Assistant 比例: {metrics['user_assistant_ratio']:.2f}")
    
    print(f"\n【内容类型】")
    for ct, count in list(metrics['content_type_distribution'].items())[:5]:
        print(f"  {ct}: {count} ({count/metrics['total_messages']*100:.1f}%)")
    
    print(f"\n【内容标签】")
    print(f"  包含代码: {metrics['messages_with_code']} ({metrics['code_percentage']:.1f}%)")
    print(f"  包含图片: {metrics['messages_with_image']} ({metrics['image_percentage']:.1f}%)")
    print(f"  包含链接: {metrics['messages_with_link']} ({metrics['link_percentage']:.1f}%)")
    
    print(f"\n【对话分叉】")
    print(f"  分叉节点数: {metrics['branching_nodes']} ({metrics['branching_percentage']:.1f}%)")
    print(f"  最大子节点数: {metrics['max_children']}")
    print(f"  平均子节点数: {metrics['avg_children']:.2f}")
    
    if 'avg_conversation_depth' in metrics:
        print(f"\n【对话深度】")
        print(f"  平均深度: {metrics['avg_conversation_depth']:.1f}")
        print(f"  最大深度: {metrics['max_conversation_depth']}")
        print(f"  中位数深度: {metrics['median_conversation_depth']:.1f}")
    
    print(f"\n【时间分布】")
    print(f"  日均对话数: {metrics['daily_avg_conversations']:.1f}")
    print(f"  日均消息数: {metrics['daily_avg_messages']:.1f}")
    print(f"  最活跃时段: {metrics['most_active_hour']}:00")
    print(f"  最不活跃时段: {metrics['least_active_hour']}:00")
    
    print(f"\n【工具使用】")
    print(f"  Tool 消息数: {metrics['tool_usage_count']} ({metrics['tool_usage_percentage']:.1f}%)")
    
    if 'model_distribution' in metrics and metrics['model_distribution']:
        print(f"\n【模型使用】")
        print(f"  最常用模型: {metrics['most_used_model']}")
        for model, count in list(metrics['model_distribution'].items())[:3]:
            print(f"  {model}: {count}")
    
    print("\n" + "="*80)


def create_simple_visualizations(messages_df, output_dir='.'):
    """创建简单的可视化图表"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. 角色分布饼图
    plt.figure(figsize=(10, 6))
    role_counts = messages_df['role'].value_counts()
    plt.pie(role_counts.values, labels=role_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('消息角色分布')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/01_role_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 2. 内容类型分布（Top 10）
    plt.figure(figsize=(12, 6))
    content_counts = messages_df['content_type'].value_counts().head(10)
    plt.barh(range(len(content_counts)), content_counts.values)
    plt.yticks(range(len(content_counts)), content_counts.index)
    plt.xlabel('消息数量')
    plt.title('内容类型分布 (Top 10)')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/02_content_type_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 3. 对话长度分布
    plt.figure(figsize=(10, 6))
    conv_lengths = messages_df.groupby('conversation_id').size()
    plt.hist(conv_lengths, bins=50, edgecolor='black', alpha=0.7)
    plt.xlabel('每条对话的消息数')
    plt.ylabel('对话数量')
    plt.title('对话长度分布')
    plt.axvline(conv_lengths.mean(), color='red', linestyle='--', label=f'平均值: {conv_lengths.mean():.1f}')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{output_dir}/03_conversation_length_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 4. 活跃时段热力图（小时 × 星期）
    plt.figure(figsize=(12, 6))
    hour_day = messages_df.groupby(['day_of_week', 'hour']).size().reset_index(name='count')
    hour_day_pivot = hour_day.pivot(index='day_of_week', columns='hour', values='count')
    # 按星期顺序排序
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hour_day_pivot = hour_day_pivot.reindex([d for d in day_order if d in hour_day_pivot.index])
    sns.heatmap(hour_day_pivot, cmap='YlOrRd', annot=False, fmt='g', cbar_kws={'label': '消息数'})
    plt.title('活跃时段热力图 (星期 × 小时)')
    plt.xlabel('小时')
    plt.ylabel('星期')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/04_active_hours_heatmap.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 5. 内容标签统计
    plt.figure(figsize=(8, 6))
    labels = ['包含代码', '包含图片', '包含链接']
    counts = [
        messages_df['has_code'].sum(),
        messages_df['has_image'].sum(),
        messages_df['has_link'].sum()
    ]
    plt.bar(labels, counts, color=['#3498db', '#e74c3c', '#2ecc71'], alpha=0.7)
    plt.ylabel('消息数量')
    plt.title('内容标签统计')
    for i, count in enumerate(counts):
        plt.text(i, count, str(count), ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/05_content_tags.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"\n可视化图表已保存到 {output_dir}/ 目录")


def main():
    """主函数"""
    import sys
    
    print("="*80)
    print("AI 使用习惯分析")
    print("="*80)
    
    # 加载数据
    messages_df, edges_df = load_data()
    
    # 计算指标
    print("\n正在计算指标...")
    metrics = calculate_metrics(messages_df, edges_df)
    
    # 打印报告
    print_metrics_report(metrics)
    
    # 创建可视化
    output_dir = sys.argv[1] if len(sys.argv) > 1 else 'analysis_output'
    print(f"\n正在生成可视化图表...")
    create_simple_visualizations(messages_df, output_dir)
    
    # 保存指标到 JSON
    # 转换 numpy 类型为 Python 原生类型以便 JSON 序列化
    metrics_serializable = {}
    for k, v in metrics.items():
        if isinstance(v, (np.integer, np.floating)):
            metrics_serializable[k] = float(v)
        elif isinstance(v, (dict, list)):
            metrics_serializable[k] = {str(k2): (float(v2) if isinstance(v2, (np.integer, np.floating)) else v2) 
                                      for k2, v2 in v.items()} if isinstance(v, dict) else v
        else:
            metrics_serializable[k] = v
    
    with open(f'{output_dir}/metrics.json', 'w', encoding='utf-8') as f:
        json.dump(metrics_serializable, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n指标数据已保存到 {output_dir}/metrics.json")
    print("\n分析完成！")


if __name__ == "__main__":
    main()

