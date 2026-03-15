# Intranet Network Deploy - Assets

This directory contains configuration files and templates for EasyTier and mihomo deployment.

## Directory Structure

```
assets/
├── mihomo/
│   └── config.yaml.template  # Mihomo TUN mode configuration template
└── easytier/
    └── config.json           # EasyTier network configuration (optional)
```

## Usage

### Mihomo TUN Mode Configuration

The template includes a working TUN mode configuration that solves Antigravity AI chat connection issues:

```bash
# Template is automatically copied by deploy_mihomo_local.sh
# Manual copy if needed:
mkdir -p ~/.config/mihomo
cp assets/mihomo/config.yaml.template ~/.config/mihomo/config.yaml
```

**IMPORTANT**: Edit `~/.config/mihomo/config.yaml` and replace `YOUR_SUBSCRIPTION_URL_HERE` with your actual proxy subscription URL.

**Key features**:
- **TUN mode**: Transparent proxying at network layer (no environment variables needed)
- **gvisor stack**: Userspace networking for compatibility
- **fake-ip DNS**: Optimal performance with DNS hijacking
- **DoH (DNS over HTTPS)**: Encrypted DNS queries
- **Auto-route**: Automatic routing table management

### EasyTier Configuration

EasyTier typically doesn't require a config file as it's configured via command-line arguments in the deployment script. The `config.json` file is provided as a reference for advanced configurations.

## Security Notes

- Never commit actual proxy credentials or subscription URLs to version control
- Use environment variables or separate config files for sensitive data
- The mihomo config template is safe to commit (contains placeholder URL only)
