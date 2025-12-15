#!/usr/bin/env python3
"""
将 Cursor/Claude 对话 JSON 文件转换为宽数据集（wide dataset）

产出两张表：
1. messages - 每条消息一行，包含所有字段
2. edges - 每条父子关系一行，用于树可视化
"""

import json
import pandas as pd
from typing import Dict, List, Any, Optional
import sys
from pathlib import Path


def extract_text_from_parts(parts: List[Any]) -> str:
    """从 parts 数组中提取所有文本内容并拼接"""
    if not parts:
        return ""
    
    text_parts = []
    for part in parts:
        if isinstance(part, str):
            text_parts.append(part)
        elif isinstance(part, dict):
            # 可能包含 text 字段或其他文本字段
            if "text" in part:
                text_parts.append(part["text"])
            # 也可以尝试提取其他可能的文本字段
            if "content" in part:
                text_parts.append(str(part["content"]))
    
    return "\n".join(text_parts)


def detect_content_flags(parts: List[Any], text: str) -> Dict[str, bool]:
    """检测内容类型标签"""
    has_code = False
    has_image = False
    has_link = False
    
    # 检测代码块（通常在 parts 中以特定格式存在）
    if isinstance(parts, list):
        for part in parts:
            if isinstance(part, dict):
                # 检查是否有代码相关的字段
                part_str = json.dumps(part).lower()
                if "code" in part_str or "language" in part_str or "```" in part_str:
                    has_code = True
                if "image" in part_str or "image_url" in part_str:
                    has_image = True
    
    # 在文本中检测代码块标记
    if "```" in text:
        has_code = True
    
    # 检测链接
    if isinstance(text, str):
        if "http://" in text or "https://" in text or "www." in text:
            has_link = True
    
    return {
        "has_code": has_code,
        "has_image": has_image,
        "has_link": has_link
    }


def parse_conversation(conv: Dict[str, Any]) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    解析单个对话，返回 messages 和 edges 列表
    
    Args:
        conv: 对话字典，包含 mapping, title, conversation_id 等
        
    Returns:
        (messages_list, edges_list) 元组
    """
    conversation_id = conv.get("conversation_id", "")
    conversation_title = conv.get("title", "")
    conversation_create_time = conv.get("create_time")
    conversation_update_time = conv.get("update_time")
    default_model_slug = conv.get("default_model_slug")
    
    mapping = conv.get("mapping", {})
    
    messages = []
    edges = []
    
    # 遍历 mapping 中的每个节点
    for node_id, node in mapping.items():
        # 提取节点级字段
        parent_id = node.get("parent")
        children = node.get("children", [])
        msg = node.get("message")
        
        # 构建基础消息记录（即使 message 为 None 也保留节点信息）
        message_record = {
            "conversation_id": conversation_id,
            "conversation_title": conversation_title,
            "node_id": node_id,
            "parent_id": parent_id,
            "children_ids": children if isinstance(children, list) else [],
            "create_time": conversation_create_time,  # 先用会话级的
            "update_time": conversation_update_time,  # 先用会话级的
            "role": None,
            "content_type": None,
            "parts_raw": None,
            "text": "",
            "has_code": False,
            "has_image": False,
            "has_link": False,
            "metadata_raw": None,
        }
        
        # 如果存在 message，提取详细信息
        if msg is not None:
            # 提取角色
            author = msg.get("author", {})
            role = author.get("role") if isinstance(author, dict) else None
            message_record["role"] = role
            
            # 提取时间（优先使用消息级的）
            msg_create_time = msg.get("create_time")
            if msg_create_time:
                message_record["create_time"] = msg_create_time
            msg_update_time = msg.get("update_time")
            if msg_update_time:
                message_record["update_time"] = msg_update_time
            
            # 提取 content
            content = msg.get("content", {})
            if isinstance(content, dict):
                content_type = content.get("content_type")
                message_record["content_type"] = content_type
                
                parts = content.get("parts", [])
                # 保存原始 parts（JSON 字符串格式）
                message_record["parts_raw"] = json.dumps(parts) if parts else None
                
                # 提取文本
                text = extract_text_from_parts(parts)
                message_record["text"] = text
                
                # 检测内容标签
                flags = detect_content_flags(parts, text)
                message_record["has_code"] = flags["has_code"]
                message_record["has_image"] = flags["has_image"]
                message_record["has_link"] = flags["has_link"]
            else:
                # content 可能不是字典，尝试其他方式处理
                message_record["parts_raw"] = json.dumps(content) if content else None
                if isinstance(content, str):
                    message_record["text"] = content
                elif isinstance(content, list):
                    message_record["text"] = extract_text_from_parts(content)
            
            # 提取 metadata（原样保存）
            metadata = msg.get("metadata")
            if metadata:
                message_record["metadata_raw"] = json.dumps(metadata)
        
        messages.append(message_record)
        
        # 构建 edges（父子关系）
        # 为每个子节点创建一条边（从当前节点到子节点）
        if children and isinstance(children, list):
            for child_id in children:
                edges.append({
                    "conversation_id": conversation_id,
                    "parent_id": node_id,
                    "child_id": child_id
                })
    
    return messages, edges


def convert_json_to_dataset(json_file_path: str, output_dir: str = ".") -> Dict[str, pd.DataFrame]:
    """
    将 JSON 文件转换为宽数据集
    
    Args:
        json_file_path: 输入的 JSON 文件路径
        output_dir: 输出目录（默认为当前目录）
        
    Returns:
        包含 'messages' 和 'edges' 两个 DataFrame 的字典
    """
    print(f"正在读取 JSON 文件: {json_file_path}")
    
    with open(json_file_path, 'r', encoding='utf-8') as f:
        conversations = json.load(f)
    
    if not isinstance(conversations, list):
        raise ValueError(f"JSON 文件应该是一个对话列表，但得到的是: {type(conversations)}")
    
    print(f"找到 {len(conversations)} 个对话")
    
    all_messages = []
    all_edges = []
    
    # 处理每个对话
    for i, conv in enumerate(conversations):
        if (i + 1) % 100 == 0:
            print(f"处理进度: {i + 1}/{len(conversations)}")
        
        try:
            messages, edges = parse_conversation(conv)
            all_messages.extend(messages)
            all_edges.extend(edges)
        except Exception as e:
            print(f"警告: 处理第 {i + 1} 个对话时出错: {e}")
            continue
    
    print(f"共提取 {len(all_messages)} 条消息, {len(all_edges)} 条边")
    
    # 转换为 DataFrame
    messages_df = pd.DataFrame(all_messages)
    edges_df = pd.DataFrame(all_edges)
    
    # 保存为 CSV
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    messages_csv = output_path / "messages.csv"
    edges_csv = output_path / "edges.csv"
    
    print(f"正在保存 messages 到: {messages_csv}")
    messages_df.to_csv(messages_csv, index=False, encoding='utf-8-sig')
    
    print(f"正在保存 edges 到: {edges_csv}")
    edges_df.to_csv(edges_csv, index=False, encoding='utf-8-sig')
    
    print("转换完成!")
    
    return {
        "messages": messages_df,
        "edges": edges_df
    }


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python json_to_dataset.py <input_json_file> [output_dir]")
        print("示例: python json_to_dataset.py conversations.json ./output")
        sys.exit(1)
    
    json_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    if not Path(json_file).exists():
        print(f"错误: 文件不存在: {json_file}")
        sys.exit(1)
    
    try:
        datasets = convert_json_to_dataset(json_file, output_dir)
        
        print("\n数据集统计:")
        print(f"Messages DataFrame: {datasets['messages'].shape}")
        print(f"Edges DataFrame: {datasets['edges'].shape}")
        print("\nMessages 列名:")
        print(datasets['messages'].columns.tolist())
        print("\nEdges 列名:")
        print(datasets['edges'].columns.tolist())
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

