#!/usr/bin/env python3
"""
LLM Super User Assistant Setup Script
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="llm-superuser-kit",
    version="0.1.0",
    author="Oscar Chouest",
    author_email="your.email@example.com",
    description="LLM-powered system administration toolkit with built-in safety features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oschouest/Test",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Systems Administration",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "click>=8.0.0",
        "pyyaml>=6.0",
        "requests>=2.28.0",
        "psutil>=5.9.0",
        "cryptography>=3.4.8",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
        "web": [
            "flask>=2.2.0",
            "flask-cors>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "superuser-assistant=core.superuser_assistant:main",
        ],
    },
)
