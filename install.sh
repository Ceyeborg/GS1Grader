#!/bin/bash

# Detect the operating system
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unsupported"
    fi
}

# Install dependencies on Ubuntu
install_ubuntu_deps() {
    echo "Installing dependencies for Ubuntu..."
    sudo apt-get update
    sudo apt-get install -y \
        libdmtx0b \
        ffmpeg \
        libsm6 \
        libxext6
}

# Install dependencies on Mac OS
install_macos_deps() {
    echo "Installing dependencies for Mac OS..."

    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi

    brew install libdmtx
    brew install ffmpeg
}

echo "GS1Grader Installation Script"
echo "============================="

OS=$(detect_os)

if [ "$OS" == "linux" ]; then
    install_ubuntu_deps
elif [ "$OS" == "macos" ]; then
    install_macos_deps
else
    echo "Unsupported operating system: $OSTYPE"
    exit 1
fi

# Install Python package
echo "Installing GS1Grader Python package..."
pip setup.py develop

echo "Installation complete!"
