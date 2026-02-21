# Ephemera CLI

A command-line interface for Alice EVO Cloud API.

## Installation

```bash
pip install -e .
```

## Configuration

### Environment Variables

```bashexport EPHEMERA_ACCESS_KEY="access_key"
export EPHEMERA_SECRET_KEY="secret_key"
```

### Credentials File

Location: `~/.ephemera/credentials`

```
access_key=<key>
secret_key=<secret>
```

## Commands

### Account

```
ephemera profile
ephemera ssh-keys
ephemera permissions
```

### Instances

```
ephemera plans
ephemera os-images <plan_id>
ephemera list
ephemera state <instance_id>
ephemera delete <instance_id>
```

### Deploy

```
ephemera deploy --product-id <id> --os-id <id> --time <hours> [--ssh-key-id <id>] [--boot-script <base64>]
```

### Power Operations

```
ephemera power <instance_id> <action>
```

Actions: boot, shutdown, restart, poweroff

### Rebuild

```
ephemera rebuild <instance_id> --os-id <id> [--ssh-key-id <id>] [--boot-script <base64>]
```

### Renew

```
ephemera renew <instance_id> --time <hours>
```

### Remote Execution

```
ephemera exec <instance_id> "<command>"
ephemera exec-result <instance_id> <uid>
```

## Output Format

```bash
ephemera profile           # JSON output (default)
ephemera -o text profile   # Text output
```

## API Endpoints

| Method | Endpoint |
|--------|--------|
| GET | /cli/v1/account/profile |
| GET | /cli/v1/account/ssh-keys |
| GET | /cli/v1/evo/permissions |
| GET | /cli/v1/evo/plans |
| GET | /cli/v1/evo/plans/{id}/os-images |
| POST | /cli/v1/evo/instances/deploy |
| GET | /cli/v1/evo/instances |
| DELETE | /cli/v1/evo/instances/{id} |
| GET | /cli/v1/evo/instances/{id}/state |
| POST | /cli/v1/evo/instances/{id}/power |
| POST | /cli/v1/evo/instances/{id}/rebuild |
| POST | /cli/v1/evo/instances/{id}/renewals |
| POST | /cli/v1/evo/instances/{id}/exec |
| GET | /cli/v1/evo/instances/{id}/exec/{uid} |

## Base URL

https://app.alice.ws

#{ Authentication

Method: Bearer Token

Header: `Authorization: Bearer <access_key>:<secret_key>`

Required headers: Authorization, Content-Type, User-Agent

## Request Formats

### Deploy Instance

```json
{"product_id": 38, "os_id": 1, "time": 24, "ssh_key_id": null, "boot_script": null}
```

### Power Operation

```'action": "shutdown'```

Actions: boot, shutdown, restart, poweroff

### Renew Instance

```
{"time": 12}
```

### Execute Command

```
{"command": "<base64_encoded_command>"}
```

## Response Format

```{"code": 200, "data": {}, "message": ""}```

#{ Plans

| ID | Name | CPU | RAM | Disk |
|----|------|-----|-----|------|
| 38 | SLC.Evo.Micro | 2 | 4GB | 60GB |
| 39 | SLC.Evo.Standard | 4 | 8GB | 120GB |
| 40 | SLC.Evo.Pro | 8 | 16GB | 200GB |
| 41 | SLC.Evo.Ultra | 16 | 32GB | 300GB |
| 42 | SLC.Evo.GPU-Ultra | 8 | 32GB | 1TB |

#{ OS Images
~| ID | Name |
|----|-----|
| 1 | Debian 12 (Bookworm) Minimal |
| 2 | Debian 11 (Bullseye) Minimal |
| 3 | Ubuntu Server 20.04 LTS Minimal |
| 4 | Ubuntu Server 22.04 LTS Minimal |
| 5 | CentOS 7 Minimal |
| 6 | CentOS Stream 9 Minimal |
| 7 | AlmaLinux 8 Minimal |
| 8 | AlmaLinux 9 Latest |
| 9 | Alpine Linux 3.19 |
| 10 | Debian 12 DevKit |
| 13 | Debian 13 (Trixie) Minimal |

## Requirements

- Python 3.7+
- No external dependencies

## Repository

https://github.com/SakuraNekooo/ephemera-cli