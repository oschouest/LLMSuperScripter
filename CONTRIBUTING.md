# Contributing to LLMSuperScripter

Thank you for your interest in contributing to LLMSuperScripter! This project aims to make system administration safer and more accessible through AI assistance.

## 🎯 Project Goals

- **Safety First**: All features must include proper safeguards and rollback capabilities
- **User Consent**: Administrative actions require clear explanation and user approval
- **Cross-Platform**: Support Windows, Linux, and macOS
- **Privacy Focused**: Support for local LLMs to keep operations private

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone git@github.com:yourusername/Test.git
   cd Test
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]  # Install development dependencies
   ```
4. **Run tests** to ensure everything works:
   ```bash
   python -m pytest
   ```

## 🔧 Development Setup

### Environment
- Python 3.8+
- Git
- Your favorite editor (VS Code recommended)

### Code Style
- Use `black` for formatting: `black .`
- Use `flake8` for linting: `flake8 .`
- Use `mypy` for type checking: `mypy .`

## 📝 Contribution Guidelines

### Pull Requests
1. Create a feature branch: `git checkout -b feature-name`
2. Make your changes with proper tests
3. Ensure all tests pass
4. Update documentation if needed
5. Submit a pull request with a clear description

### Code Requirements
- **Safety Checks**: All administrative operations must include backup/rollback
- **Logging**: All actions must be logged with clear audit trails
- **Error Handling**: Graceful error handling with user-friendly messages
- **Documentation**: Clear docstrings and comments
- **Tests**: Unit tests for new functionality

### Security Considerations
- **Input Validation**: Sanitize all user inputs
- **Privilege Escalation**: Clear warnings and consent for admin operations
- **Credential Handling**: Secure storage and handling of sensitive data
- **Command Injection**: Prevent shell injection vulnerabilities

## 🏗️ Architecture Guidelines

### Module Structure
```
modules/
├── your_module/
│   ├── __init__.py
│   ├── operations.py    # Core functionality
│   ├── safety.py        # Backup/rollback logic
│   └── tests/           # Module tests
```

### Safety Engine Integration
All modules must integrate with the core safety engine:
- Use `create_backup()` before modifications
- Implement `rollback()` functionality
- Provide clear operation descriptions
- Include validation steps

## 🧪 Testing

### Test Categories
- **Unit Tests**: Test individual functions
- **Integration Tests**: Test module interactions
- **Safety Tests**: Test backup/rollback functionality
- **Security Tests**: Test input validation and security

### Running Tests
```bash
# All tests
python -m pytest

# Specific module
python -m pytest tests/test_module_name.py

# With coverage
python -m pytest --cov=core --cov=modules
```

## 📚 Documentation

### Required Documentation
- **Module README**: Purpose, usage examples, safety considerations
- **API Documentation**: Docstrings for all public functions
- **Safety Procedures**: Clear backup/rollback documentation
- **Examples**: Working examples for common use cases

## 🐛 Bug Reports

When reporting bugs, please include:
- **Operating System** and version
- **Python version**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Error messages** (if any)
- **System logs** (if relevant)

## 💡 Feature Requests

For new features, please provide:
- **Use case description**
- **Safety considerations**
- **Cross-platform compatibility**
- **Integration with existing modules**

## 🔒 Security

If you discover security vulnerabilities:
1. **DO NOT** create a public issue
2. Email the maintainers directly
3. Provide detailed reproduction steps
4. Allow time for responsible disclosure

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and community interaction
- **Documentation**: Check the `docs/` directory

## 🏆 Recognition

Contributors will be recognized in:
- **CONTRIBUTORS.md** file
- **Release notes** for significant contributions
- **Module documentation** for module authors

Thank you for helping make system administration safer and more accessible! 🚀
