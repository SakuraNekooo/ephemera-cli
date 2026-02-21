#!/usr/bin/env python3
"""Ephemera CLI - Alice EVO Cloud API Client by Atri"""
import argparse, json, base64, sys, os
from typing import Optional, Dict, Any
import urllib.request, urllib.error

__version__ = "1.0.0"

class EphemeraClient:
    def __init__(self, access_key: str, secret_key: str, base_url: str = "https://app.alice.ws"):
        self.token = f"{access_key}:{secret_key}"
        self.base_url = base_url.rstrip("/")

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        req_data = json.dumps(data).encode() if data else None
        request = urllib.request.Request(url, data=req_data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if e.fp else ""
            try:
                return {"error": True, "code": e.code, "message": json.loads(error_body).get("message", error_body)}
            except:
                return {"error": True, "code": e.code, "message": error_body}
        except Exception as e:
            return {"error": True, "message": str(e)}

    def get_profile(self): return self._request("GET", "/cli/v1/account/profile")
    def get_ssh_keys(self): return self._request("GET", "/cli/v1/account/ssh-keys")
    def get_permissions(self): return self._request("GET", "/cli/v1/evo/permissions")
    def get_plans(self): return self._request("GET", "/cli/v1/evo/plans")
    def get_os_images(self, plan_id): return self._request("GET", f"/cli/v1/evo/plans/{plan_id}/os-images")
    def list_instances(self): return self._request("GET", "/cli/v1/evo/instances")
    def delete_instance(self, instance_id): return self._request("DELETE", f"/cli/v1/evo/instances/{instance_id}")
    def get_instance_state(self, instance_id): return self._request("GET", f"/cli/v1/evo/instances/{instance_id}/state")

    def deploy_instance(self, product_id, os_id, time, ssh_key_id=None, boot_script=None):
        data = {"product_id": product_id, "os_id": os_id, "time": time}
        if ssh_key_id: data["ssh_key_id"] = ssh_key_id
        if boot_script: data["boot_script"] = boot_script
        return self._request("POST", "/cli/v1/evo/instances/deploy", data)

    def power_operation(self, instance_id, action):
        return self._request("POST", f"/cli/v1/evo/instances/{instance_id}/power", {"action": action})

    def rebuild_instance(self, instance_id, os_id, ssh_key_id=None, boot_script=None):
        data = {"os_id": os_id}
        if ssh_key_id: data["ssh_key_id"] = ssh_key_id
        if boot_script: data["boot_script"] = boot_script
        return self._request("POST", f"/cli/v1/evo/instances/{instance_id}/rebuild", data)

    def renew_instance(self, instance_id, time):
        return self._request("POST", f"/cli/v1/evo/instances/{instance_id}/renewals", {"time": time})

    def exec_command(self, instance_id, command):
        if not command.startswith("eyJ"):
            command = base64.b64encode(command.encode()).decode()
        return self._request("POST", f"/cli/v1/evo/instances/{instance_id}/exec", {"command": command})

    def get_exec_result(self, instance_id, command_uid):
        return self._request("GET", f"/cli/v1/evo/instances/{instance_id}/exec/{command_uid}")

def print_result(result, output_format="json"):
    if result.get("error"):
        print(f"Error: {result.get('message', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)
    if output_format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if "data" in result:
            data = result["data"]
            if isinstance(data, list):
                for item in data:
                    print("-" * 50)
                    if isinstance(item, dict):
                        for k, v in item.items(): print(f"{k}: {v}")
            elif isinstance(data, dict):
                for k, v in data.items(): print(f"{k}: {v}")
        else:
            print(result.get("message", "Success"))

def load_credentials():
    access_key = os.environ.get("EPHEMERA_ACCESS_KEY")
    secret_key = os.environ.get("EPHEMERA_SECRET_KEY")
    if access_key and secret_key:
        return access_key, secret_key
    config_file = os.path.expanduser("~/.ephemera/credentials")
    if os.path.exists(config_file):
        with open(config_file) as f:
            for line in f:
                if line.startswith("access_key="): access_key = line.strip().split("=", 1)[1]
                elif line.startswith("secret_key="): secret_key = line.strip().split("=", 1)[1]
        if access_key and secret_key:
            return access_key, secret_key
    return None, None

def main():
    parser = argparse.ArgumentParser(description="Ephemera CLI - Alice EVO Cloud API")
    parser.add_argument("--version", action="version", version=f"Ephemera CLI {__version__}")
    parser.add_argument("--access-key", help="API Access Key")
    parser.add_argument("--secret-key", help="API Secret Key")
    parser.add_argument("-o", "--output", choices=["json", "text"], default="json")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("profile")
    sub.add_parser("ssh-keys")
    sub.add_parser("permissions")
    sub.add_parser("plans")
    sub.add_parser("list")

    p = sub.add_parser("os-images")
    p.add_argument("plan_id", type=int)

    p = sub.add_parser("deploy")
    p.add_argument("--product-id", required=True, type=int)
    p.add_argument("--os-id", required=True, type=int)
    p.add_argument("--time", required=True, type=int)
    p.add_argument("--ssh-key-id", type=int)
    p.add_argument("--boot-script")

    p = sub.add_parser("delete")
    p.add_argument("instance_id", type=int)

    p = sub.add_parser("state")
    p.add_argument("instance_id", type=int)

    p = sub.add_parser("power")
    p.add_argument("instance_id", type=int)
    p.add_argument("action", choices=["boot", "shutdown", "restart", "poweroff"])

    p = sub.add_parser("rebuild")
    p.add_argument("instance_id", type=int)
    p.add_argument("--os-id", required=True, type=int)
    p.add_argument("--ssh-key-id", type=int)
    p.add_argument("--boot-script")

    p = sub.add_parser("renew")
    p.add_argument("instance_id", type=int)
    p.add_argument("--time", required=True, type=int)

    p = sub.add_parser("exec")
    p.add_argument("instance_id", type=int)
    p.add_argument("command")
    p.add_argument("--raw", action="store_true")

    p = sub.add_parser("exec-result")
    p.add_argument("instance_id", type=int)
    p.add_argument("command_uid")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return

    access_key, secret_key = args.access_key, args.secret_key
    if not access_key or not secret_key:
        access_key, secret_key = load_credentials()
    if not access_key or not secret_key:
        print("Error: No credentials provided", file=sys.stderr)
        sys.exit(1)

    client = EphemeraClient(access_key, secret_key)
    cmds = {
        "profile": lambda: client.get_profile(),
        "ssh-keys": lambda: client.get_ssh_keys(),
        "permissions": lambda: client.get_permissions(),
        "plans": lambda: client.get_plans(),
        "os-images": lambda: client.get_os_images(args.plan_id),
        "list": lambda: client.list_instances(),
        "delete": lambda: client.delete_instance(args.instance_id),
        "state": lambda: client.get_instance_state(args.instance_id),
        "power": lambda: client.power_operation(args.instance_id, args.action),
        "renew": lambda: client.renew_instance(args.instance_id, args.time),
        "exec": lambda: client.exec_command(args.instance_id, args.command),
        "exec-result": lambda: client.get_exec_result(args.instance_id, args.command_uid),
        "deploy": lambda: client.deploy_instance(args.product_id, args.os_id, args.time, args.ssh_key_id, args.boot_script),
        "rebuild": lambda: client.rebuild_instance(args.instance_id, args.os_id, args.ssh_key_id, args.boot_script),
    }
    print_result(cmds[args.cmd](), args.output)

if __name__ == "__main__":
    main()
