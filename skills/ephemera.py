#!/usr/bin/env python3
"""
Ephemera Skill for AstrBot
Interact with Alice EVO Cloud API through chat commands
"""

import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ephemera_cli import EphemeraClient, load_credentials

TRIGGER = "!evo"

def get_client():
    """Get Ephemera client with credentials"""
    access_key, secret_key = load_credentials()
    if not access_key or not secret_key:
        return None, "未配置凭证。请设置 EPHEMERA_ACCESS_KEY 和 EPHEMERA_SECRET_KEY 环境变量"
    return EphemeraClient(access_key, secret_key), None

def format_output(result):
    """Format API result for chat output"""
    if result.get("error"):
        return f"❌ 错误: {result.get('message', '未知错误')}"

    data = result.get("data")
    message = result.get("message", "")

    if data is None:
        return f"✅ {message}" if message else "✅ 成功"

    if isinstance(data, list):
        if len(data) == 0:
            return "📭 没有数据"
        output = []
        for item in data[:10]:  # Limit to 10 items
            if isinstance(item, dict):
                name = item.get("name") or item.get("id") or item.get("username") or "?"
                output.append(f"• {name}")
        if len(data) > 10:
            output.append(f"... 还有 {len(data) - 10} 项")
        return "\n".join(output)

    if isinstance(data, dict):
        output = []
        for key, value in list(data.items())[:10]:
            if isinstance(value, (str, int, float, bool)):
                output.append(f"{key}: {value}")
            elif value is None:
                output.append(f"{key}: null")
        return "\n".join(output)

    return str(data)

async def handle_message(message, args):
    """Handle incoming message"""
    if not message.startswith(TRIGGER):
        return None

    parts = message.split(maxsplit=2)
    if len(parts) < 2:
        return f"""Ephemera CLI 命令:
{TRIGGER} profile - 获取账户信息
{TRIGGER} plans - 查看可用计划
{TRIGGER} list - 列出实例
{TRIGGER} state <id> - 查看实例状态
{TRIGGER} deploy <plan> <os> <hours> - 部署实例
{TRIGGER} delete <id> - 删除实例
{TRIGGER} power <id> <action> - 电源操作
{TRIGGER} renew <id> <hours> - 续费实例"""

    cmd = parts[1]
    client, error = get_client()
    if error:
        return error

    result = None

    if cmd == "profile":
        result = client.get_profile()
    elif cmd == "plans":
        result = client.get_plans()
    elif cmd == "list":
        result = client.list_instances()
    elif cmd == "permissions":
        result = client.get_permissions()
    elif cmd in ["state", "delete", "power", "renew", "deploy"]:
        if len(parts) < 3:
            return f"❌ 缺少参数。用法: {TRIGGER} {cmd} ..."

        sub_args = parts[2].split()

        if cmd == "state":
            instance_id = int(sub_args[0])
            result = client.get_instance_state(instance_id)
        elif cmd == "delete":
            instance_id = int(sub_args[0])
            result = client.delete_instance(instance_id)
        elif cmd == "power":
            instance_id = int(sub_args[0])
            action = sub_args[1] if len(sub_args) > 1 else "shutdown"
            result = client.power_operation(instance_id, action)
        elif cmd == "renew":
            instance_id = int(sub_args[0])
            time = int(sub_args[1]) if len(sub_args) > 1 else 1
            result = client.renew_instance(instance_id, time)
        elif cmd == "deploy":
            if len(sub_args) < 3:
                return f"❌ 用法: {TRIGGER} deploy <plan_id> <os_id> <hours>"
            plan_id = int(sub_args[0])
            os_id = int(sub_args[1])
            hours = int(sub_args[2])
            result = client.deploy_instance(plan_id, os_id, hours)
    else:
        return f"❌ 未知命令: {cmd}"

    return format_output(result) if result else "❌ 无响应"

def init():
    """Initialize skill"""
    print("Ephemera skill initialized")

def cleanup():
    """Cleanup skill"""
    print("Ephemera skill cleaned up")

__all__ = ["init", "cleanup", "handle_message", "TRIGGER"]
