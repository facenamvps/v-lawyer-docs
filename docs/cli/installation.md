---
id: installation
title: Installation
sidebar_label: Installation
sidebar_position: 1
---

# Installing Kanuni CLI

The Kanuni CLI can be installed on macOS, Linux, and Windows. Choose your preferred installation method below.

## System Requirements

- **Operating System**: macOS 10.15+, Linux (Ubuntu 18.04+, CentOS 7+), Windows 10+
- **Memory**: Minimum 512MB RAM
- **Storage**: 100MB free disk space
- **Network**: Internet connection for API calls

## Installation Methods

### Option 1: Install from Binary (Recommended)

The fastest way to install Kanuni is to download the pre-compiled binary for your platform.

#### macOS

```bash
# Download the latest release
curl -L https://github.com/v-lawyer/kanuni-cli/releases/latest/download/kanuni-darwin-amd64 -o kanuni

# Make it executable
chmod +x kanuni

# Move to PATH
sudo mv kanuni /usr/local/bin/

# Verify installation
kanuni --version
```

For Apple Silicon (M1/M2/M3):

```bash
# Download the ARM64 version
curl -L https://github.com/v-lawyer/kanuni-cli/releases/latest/download/kanuni-darwin-arm64 -o kanuni

# Make it executable
chmod +x kanuni

# Move to PATH
sudo mv kanuni /usr/local/bin/

# Verify installation
kanuni --version
```

#### Linux

```bash
# Download the latest release
curl -L https://github.com/v-lawyer/kanuni-cli/releases/latest/download/kanuni-linux-amd64 -o kanuni

# Make it executable
chmod +x kanuni

# Move to PATH
sudo mv kanuni /usr/local/bin/

# Verify installation
kanuni --version
```

#### Windows

1. Download the latest release from [GitHub Releases](https://github.com/v-lawyer/kanuni-cli/releases/latest)
2. Extract `kanuni.exe` from the ZIP file
3. Add the directory containing `kanuni.exe` to your PATH environment variable
4. Open a new Command Prompt or PowerShell and verify:

```powershell
kanuni --version
```

### Option 2: Install via Homebrew (macOS/Linux)

If you have [Homebrew](https://brew.sh/) installed:

```bash
# Add the V-Lawyer tap
brew tap v-lawyer/kanuni

# Install Kanuni
brew install kanuni

# Verify installation
kanuni --version
```

### Option 3: Install via Cargo (Rust)

If you have [Rust](https://rustup.rs/) installed:

```bash
# Install from crates.io
cargo install kanuni

# Verify installation
kanuni --version
```

### Option 4: Build from Source

For developers who want to build from source:

```bash
# Clone the repository
git clone https://github.com/v-lawyer/kanuni-cli.git
cd kanuni-cli

# Build the project
cargo build --release

# The binary will be in target/release/kanuni
./target/release/kanuni --version

# Optionally, install to PATH
cargo install --path .
```

## Post-Installation Setup

### 1. Shell Completions (Optional)

Generate shell completions for your shell to enable tab completion:

#### Bash

```bash
kanuni completions bash > ~/.kanuni-completions.bash
echo "source ~/.kanuni-completions.bash" >> ~/.bashrc
source ~/.bashrc
```

#### Zsh

```bash
kanuni completions zsh > ~/.kanuni-completions.zsh
echo "source ~/.kanuni-completions.zsh" >> ~/.zshrc
source ~/.zshrc
```

#### Fish

```bash
kanuni completions fish > ~/.config/fish/completions/kanuni.fish
```

#### PowerShell

```powershell
kanuni completions powershell | Out-String | Invoke-Expression
```

### 2. Configuration

Kanuni stores its configuration in:
- **macOS/Linux**: `~/.config/kanuni/config.toml`
- **Windows**: `%APPDATA%\kanuni\config.toml`

You can initialize the configuration with:

```bash
kanuni config show
```

### 3. Authentication

After installation, you'll need to authenticate with V-Lawyer:

```bash
kanuni auth login
```

See the [Authentication Guide](./authentication/overview) for details.

## Updating Kanuni

### Using Homebrew

```bash
brew upgrade kanuni
```

### Using Cargo

```bash
cargo install kanuni --force
```

### Manual Update

Follow the same steps as installation, but replace the existing binary.

## Uninstallation

### Using Homebrew

```bash
brew uninstall kanuni
```

### Using Cargo

```bash
cargo uninstall kanuni
```

### Manual Uninstallation

1. Remove the binary:
   - **macOS/Linux**: `sudo rm /usr/local/bin/kanuni`
   - **Windows**: Delete `kanuni.exe` from its location

2. Remove configuration and data (optional):
   - **macOS/Linux**: `rm -rf ~/.config/kanuni`
   - **Windows**: Delete `%APPDATA%\kanuni`

## Troubleshooting

### Command Not Found

If you get "command not found" after installation:

1. Ensure the binary is in your PATH:
   ```bash
   echo $PATH
   ```

2. Add the directory to your PATH if needed:
   ```bash
   export PATH="$PATH:/usr/local/bin"
   ```

### Permission Denied

If you get "permission denied" errors:

```bash
chmod +x /usr/local/bin/kanuni
```

### SSL Certificate Issues

If you encounter SSL certificate errors:

```bash
# macOS
brew install ca-certificates

# Linux
sudo apt-get install ca-certificates  # Debian/Ubuntu
sudo yum install ca-certificates       # CentOS/RHEL
```

## Next Steps

Now that you have Kanuni installed, you can:

- [Set up authentication](./authentication/overview)
- [Learn basic commands](./commands/overview)
- [Configure your environment](./advanced/config-file)

## Getting Help

If you encounter any issues:

- Check the [GitHub Issues](https://github.com/v-lawyer/kanuni-cli/issues)
- Join our [Discord community](https://discord.gg/v-lawyer)
- Email support: support@v-lawyer.ai