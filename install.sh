#!/bin/bash

set -e

echo "🔧 Installing system & Python dependencies for proxy-hunter..."

# Detect OS
OS=""
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    OS=$(uname -s)
fi

# Install zmap
install_zmap() {
    echo "[*] Installing zmap..."
    case "$OS" in
        ubuntu|debian)
            sudo apt update && sudo apt install -y zmap
            ;;
        arch)
            sudo pacman -Syu --noconfirm zmap
            ;;
        centos|rhel|fedora)
            sudo yum install -y epel-release
            sudo yum install -y zmap
            ;;
        darwin)
            echo "[*] macOS detected. Using Homebrew to install zmap..."
            brew install zmap
            ;;
        *)
            echo "[!] Unknown or unsupported OS: $OS"
            echo "    Please install zmap manually."
            ;;
    esac
}

# Install Python dependencies
install_python_packages() {
    echo "[*] Installing Python dependencies..."
    python3 -m pip install --upgrade pip
    python3 -m pip install requests
}

# Run installers
install_zmap
install_python_packages

echo "✅ Installation complete."
