#!/bin/bash

# LLMSuperScripter Laptop Setup Script
# Quick setup for transferring development environment to laptop

echo "🚀 LLMSuperScripter Laptop Setup"
echo "================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git not installed. Installing..."
    sudo apt update && sudo apt install -y git
fi

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not installed. Installing..."
    sudo apt update && sudo apt install -y python3 python3-pip
fi

# Check if VS Code is installed
if ! command -v code &> /dev/null; then
    echo "❌ VS Code not installed. Would you like to install it? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        # Install VS Code
        wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
        sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
        sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
        sudo apt update && sudo apt install -y code
    fi
fi

# Clone the repository
echo "📦 Cloning LLMSuperScripter repository..."
if [ -d "LLMSuperScripter" ]; then
    echo "⚠️  Directory already exists. Updating..."
    cd LLMSuperScripter && git pull
else
    git clone git@github.com:oschouest/Test.git LLMSuperScripter
    cd LLMSuperScripter
fi

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip3 install -r requirements.txt

# Install the package in development mode
echo "⚙️  Installing LLMSuperScripter..."
pip3 install -e .

# Test the installation
echo "🧪 Testing installation..."
python3 -c "import core.superscripter; print('✅ LLMSuperScripter imported successfully')"

# Open in VS Code
echo "🖥️  Opening in VS Code..."
code .

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Configure your LLM API keys (if using OpenAI)"
echo "   2. Test with: python3 core/superscripter.py --snapshots"
echo "   3. Start scripting with AI assistance!"
echo ""
echo "🔗 Repository: https://github.com/oschouest/LLMSuperScripter"
echo "📚 Documentation: Check the README.md"
