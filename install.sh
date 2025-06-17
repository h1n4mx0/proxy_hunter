#!/bin/bash

set -e

echo "🔧 Installing full environment for proxy-hunter..."

# Detect OS
OS=""
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    OS=$(uname -s)
fi

# Install zmap, masscan, curl, jq
install_system_packages() {
    echo "[*] Installing system tools (zmap, masscan, curl, jq)..."
    case "$OS" in
        ubuntu|debian)
            sudo apt update
            sudo apt install -y zmap masscan curl jq python3 python3-pip python3-venv
            ;;
        arch)
            sudo pacman -Syu --noconfirm zmap masscan curl jq python python-pip python-virtualenv
            ;;
        centos|rhel|fedora)
            sudo yum install -y epel-release
            sudo yum install -y zmap masscan curl jq python3 python3-pip python3-virtualenv
            ;;
        darwin)
            echo "[*] macOS detected. Using Homebrew..."
            brew install zmap masscan curl jq python
            ;;
        *)
            echo "[!] Unknown or unsupported OS: $OS"
            echo "    Please install zmap, masscan, curl, jq, and python3 manually."
            exit 1
            ;;
    esac
}

# Setup virtual environment (optional)
setup_venv() {
    echo "[*] Creating Python virtual environment in ./venv ..."
    python3 -m venv venv
    source venv/bin/activate
    echo "[*] Installing Python packages in venv..."
    pip install --upgrade pip
    pip install requests
}

# Main
install_system_packages
setup_venv

echo -e "\n✅ All dependencies installed."
echo "👉 To activate the environment later, run:"
echo "   source venv/bin/activate"
