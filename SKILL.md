# Ephemera CLI Skill

A Claude-compatible skill for interacting with Alice EVO Cloud API (Ephemera).

## Description

This skill enables Claude to manage Ephemera cloud instances through natural language commands. Users can deploy, monitor, and control EVO instances using conversational interfaces.

## Capabilities

- **Account Management**: View profile, SSH keys, and permissions
- **Instance Lifecycle**: Deploy, list, monitor, and delete instances
- **Power Control**: Boot, shutdown, restart, and force poweroff
- **Instance Operations**: Rebuild OS, renew duration, execute remote commands
- **Resource Discovery**: List available plans, OS images, and configurations

## Configuration

### Credentials Setup

Set environment variables before using this skill:

```bash
export EPHEMERA_ACCESS_KEY="your_access_key"
export EPHEMERA_SECRET_KEY="your_secret_key"
```

Or create a credentials file at `~/.ephemera/credentials`:

```
access_key=your_access_key
secret_key=your_secret_key
```

### Authentication

- **Method**: Bearer Token
- **Format**: `access_key:secret_key`
- **Required Headers**: `Authorization`, `Content-Type`, `User-Agent`

## Usage Examples

### Natural Language Commands

#### Account Information

```
"Show my Ephemera account details"
"What's my current credit balance?"
"List my SSH keys"
```

#### Instance Management

```
"Deploy a new EVO Micro instance with Debian 12 for 24 hours"
"List all my running instances"
"Show the status of instance 12345"
"Delete instance 12345"
```

#### Power Operations

```
"Shutdown instance 12345"
"Restart instance 12345"
"Power off instance 12345 immediately"
"Boot up instance 12345"
```

#### Instance Operations

```
"Rebuild instance 12345 with Ubuntu 22.04"
"Extend instance 12345 for another 12 hours"
"Run 'uptime' command on instance 12345"
```

### Direct CLI Commands

```bash
# Account
ephemera profile
ephemera ssh-keys
ephemera permissions

# Plans & Images
ephemera plans
ephemera os-images 38

# Instances
ephemera list
ephemera state 12345
ephemera deploy --product-id 38 --os-id 1 --time 24
ephemera power 12345 shutdown
ephemera renew 12345 --time 12
ephemera rebuild 12345 --os-id 3
ephemera delete 12345

# Remote Execution
ephemera exec 12345 "docker ps"
ephemera exec-result 12345 <command_uid>
```

## API Reference

### Base URL
```
https://app.alice.ws
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cli/v1/account/profile` | Get user profile |
| GET | `/cli/v1/account/ssh-keys` | List SSH keys |
| GET | `/cli/v1/evo/permissions` | Get user permissions |
| GET | `/cli/v1/evo/plans` | List available plans |
| GET | `/cli/v1/evo/plans/{id}/os-images` | Get OS images for plan |
| POST | `/cli/v1/evo/instances/deploy` | Deploy new instance |
| GET | `/cli/v1/evo/instances` | List all instances |
| GET | `/cli/v1/evo/instances/{id}` | Get instance details |
| GET | `/cli/v1/evo/instances/{id}/state` | Get instance state |
| POST | `/cli/v1/evo/instances/{id}/power` | Power operation |
| POST | `/cli/v1/evo/instances/{id}/rebuild` | Rebuild instance |
| POST | `/cli/v1/evo/instances/{id}/renewals` | Renew instance |
| POST | `/cli/v1/evo/instances/{id}/exec` | Execute command |
| GET | `/cli/v1/evo/instances/{id}/exec/{uid}` | Get command result |
| DELETE | `/cli/v1/evo/instances/{id}` | Delete instance |

### Request Parameters

#### Deploy Instance
```json
{
  "product_id": 38,
  "os_id": 1,
  "time": 24,
  "ssh_key_id": null,
  "boot_script": "<base64_encoded_script>"
}
```

#### Power Operation
```json
{
  "action": "shutdown"
}
```
Actions: `boot`, `shutdown`, `restart`, `poweroff`

#### Renew Instance
```json
{
  "time": 12
}
```

#### Execute Command
```json
{
  "command": "<base64_encoded_command>"
}
```

### Response Format

```json
{
  "code": 200,
  "data": { /* response data */ },
  "message": "Success"
}
```

## Available Plans

| ID | Name | CPU | RAM | Disk | Speed |
|----|------|-----|-----|------|-------|
| 38 | SLC.Evo.Micro | 2 | 4GB | 60GB | 500/5000 Mbps |
| 39 | SLC.Evo.Standard | 4 | 8GB | 120GB | 500/5000 Mbps |
| 40 | SLC.Evo.Pro | 8 | 16GB | 200GB | 500/5000 Mbps |
| 41 | SLC.Evo.Ultra | 16 | 32GB | 300GB | 500/5000 Mbps |
| 42 | SLC.Evo.GPU-Ultra | 8 | 32GB | 1TB | 500/5000 Mbps + GPU |

## Available OS Images

### Debian
- Debian 12 (Bookworm) Minimal (ID: 1)
- Debian 11 (Bullseye) Minimal (ID: 2)
- Debian 12 DevKit (ID: 10)
- Debian 13 (Trixie) Minimal (ID: 13)

### Ubuntu
- Ubuntu Server 20.04 LTS Minimal (ID: 3)
- Ubuntu Server 22.04 LTS Minimal (ID: 4)

### AlmaLinux
- AlmaLinux 8 Minimal (ID: 7)
- AlmaLinux 9 Latest (ID: 8)

### Alpine Linux
- Alpine Linux 3.19 (ID: 9)

### CentOS
- CentOS 7 Minimal (ID: 5)
- CentOS Stream 9 Minimal (ID: 6)

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| 401 | Unauthorized | Check credentials |
| 403 | Forbidden | Verify permissions |
| 404 | Not Found | Check resource ID |
| 429 | Rate Limited | Wait and retry |
| 500 | Server Error | Retry or contact support |

## Security Considerations

1. **Credentials**: Never hardcode credentials in scripts
2. **SSH Keys**: Use SSH keys for secure instance access
3. **Boot Scripts**: Base64 encode sensitive scripts
4. **Instance Access**: Change default passwords after deployment
5. **Firewall**: Configure security groups appropriately

## Example Workflows

### Deploy and Configure Instance

```bash
# 1. List available plans
ephemera plans

# 2. Get OS images for chosen plan
ephemera os-images 38

# 3. Deploy instance
ephemera deploy --product-id 38 --os-id 1 --time 24

# 4. Check instance status
ephemera state 12345

# 5. Execute configuration script
ephemera exec 12345 "apt update && apt install -y docker.io"

# 6. Renew if needed
ephemera renew 12345 --time 12
```

### Monitor and Manage Instances

```bash
# List all instances
ephemera list

# Monitor specific instance
ephemera state 12345

# Graceful shutdown
ephemera power 12345 shutdown

# Force poweroff if needed
ephemera power 12345 poweroff

# Clean up
ephemera delete 12345
```

## Troubleshooting

### Common Issues

**Authentication Failed**
- Verify access key and secret key
- Check credentials file permissions
- Ensure no extra whitespace in credentials

**Instance Deployment Failed**
- Check available stock for plan
- Verify OS image ID is valid for plan
- Check user permissions and credit balance

**Command Execution Timeout**
- Instance may be booting
- Check instance state first
- Wait for instance to be fully ready

**Rate Limiting**
- Reduce request frequency
- Implement exponential backoff
- Cache plan and OS image data

## Dependencies

- Python 3.7+
- No external dependencies (uses only Python standard library)

## License

MIT License

## Author

柏喵Atri

## Version

1.0.0

## GitHub Repository

https://github.com/SakuraNekooo/ephemera-cli
