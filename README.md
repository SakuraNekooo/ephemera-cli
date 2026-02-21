# Ephemera CLI

A command-line interface for Alice EVO Cloud API (Ephemera API 2.0).

## Installation

```bash
pip install ephemera-cli
```

Or install from source:
```bash
git clone https://github.com/SakuraNekooo/ephemera-cli.git
cd ephemera-cli
pip install -e .
```

## Configuration

Set credentials via environment variables:
```bash
export EPHEMERA_ACCESS_KEY="your_access_key"
export EPHEMERA_SECRET_KEY="your_secret_key"
```

Or create a credentials file:
```bash
mkdir -p ~/.ephemera
cat > ~/.ephemera/credentials << EOF
access_key=your_access_key
secret_key=your_secret_key
EOF
chmod 600 ~/.ephemera/credentials
```

## Usage

### Account Commands

```bash
# Get user profile
ephemera profile

# List SSH keys
ephemera ssh-keys
```

### EVO Instance Commands

```bash
# Get permissions
ephemera permissions

# List available plans
ephemera plans

# Get OS images for a plan
ephemera os-images 38

# Deploy new instance
ephemera deploy --product-id 38 --os-id 1 --time 24

# List all instances
ephemera list

# Get instance state
ephemera state 12345

# Power operations (boot/shutdown/restart/poweroff)
ephemera power 12345 shutdown

# Renew instance
ephemera renew 12345 --time 1

# Rebuild instance
ephemera rebuild 12345 --os-id 1

# Execute command on instance
ephemera exec 12345 "uptime"

# Get command execution result
ephemera exec-result 12345 <command_uid>

# Delete instance
ephemera delete 12345
```

### Output Format

Default output is JSON. Use `-o text` for plain text:
```bash
ephemera list -o text
```

### Override Credentials

```bash
ephemera --access-key KEY --secret-key SECRET profile
```

## API Reference

This CLI wraps the Ephemera API 2.0:

- Base URL: `https://app.alice.ws`
- Authentication: Bearer token (`access_key:secret_key`)

### Endpoints

| Command | Method | Endpoint |
| --- | --- | --- |
| profile | GET | /cli/v1/account/profile |
| ssh-keys | GET | /cli/v1/account/ssh-keys |
| permissions | GET | /cli/v1/evo/permissions |
| plans | GET | /cli/v1/evo/plans |
| os-images | GET | /cli/v1/evo/plans/{id}/os-images |
| deploy | POST | /cli/v1/evo/instances/deploy |
| list | GET | /cli/v1/evo/instances |
| state | GET | /cli/v1/evo/instances/{id}/state |
| power | POST | /cli/v1/evo/instances/{id}/power |
| rebuild | POST | /cli/v1/evo/instances/{id}/rebuild |
| renew | POST | /cli/v1/evo/instances/{id}/renewals |
| exec | POST | /cli/v1/evo/instances/{id}/exec |
| exec-result | GET | /cli/v1/evo/instances/{id}/exec/{uid} |
| delete | DELETE | /cli/v1/evo/instances/{id} |

## Development

```bash
# Run tests
python -m pytest tests/

# Build package
python -m build
```

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## License

MIT License

## Author

柏喵Atri
