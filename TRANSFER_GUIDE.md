# 🚀 Transfer Guide: Desktop → Laptop

## Quick Transfer Options

### Option 1: Simple Git Clone (Recommended)
**On your laptop:**
```bash
git clone git@github.com:oschouest/Test.git LLMSuperScripter
cd LLMSuperScripter
pip3 install -r requirements.txt
pip3 install -e .
code .
```

### Option 2: Use the Setup Script
**Transfer the setup script to your laptop and run:**
```bash
# Copy setup-laptop.sh to your laptop first, then:
chmod +x setup-laptop.sh
./setup-laptop.sh
```

### Option 3: Full Environment Sync

#### SSH Key Transfer
```bash
# Copy your SSH keys to laptop (if not already there)
scp ~/.ssh/id_rsa* user@laptop:~/.ssh/
```

#### VS Code Extensions (Manual)
Your key extensions for this project:
- Python extension
- GitLens
- Remote Development pack
- GitHub Copilot (if you have it)

## 🔧 Laptop Setup Checklist

- [ ] Git installed and configured
- [ ] Python 3.8+ installed
- [ ] VS Code installed
- [ ] SSH keys configured for GitHub
- [ ] Repository cloned
- [ ] Dependencies installed (`pip3 install -r requirements.txt`)
- [ ] Package installed (`pip3 install -e .`)
- [ ] Test run: `python3 core/superscripter.py --snapshots`

## 🎯 Quick Start on Laptop

1. **Clone & Setup:**
   ```bash
   git clone git@github.com:oschouest/Test.git LLMSuperScripter
   cd LLMSuperScripter
   pip3 install -r requirements.txt
   ```

2. **Test the Tool:**
   ```bash
   python3 core/superscripter.py --snapshots
   ```

3. **Open in VS Code:**
   ```bash
   code .
   ```

## 🔄 Staying in Sync

**When working on laptop:**
```bash
git pull    # Get latest changes
# ... make changes ...
git add .
git commit -m "Your changes"
git push    # Push back to GitHub
```

**When returning to desktop:**
```bash
git pull    # Get laptop changes
```

## 📁 Important Files Locations

- **Main Tool**: `core/superscripter.py`
- **Config**: `requirements.txt`, `setup.py`
- **Modules**: `modules/registry/`, `core/llm_interface.py`
- **Docs**: `README.md`, `CONTRIBUTING.md`

## 🚨 Don't Forget

- Your `.superscripter-backups/` directory stays local (not in git)
- Any API keys or secrets should be configured separately on laptop
- VS Code workspace settings will need to be reconfigured

---

**🎉 You're all set!** Your LLMSuperScripter will be ready to go on your laptop with all the same functionality.
