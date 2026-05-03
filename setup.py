from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nexus-ultimate",
    version="1.0.0",
    author="NEXUS Ultimate Team",
    author_email="nexus@example.com",
    description="Elite cognitive AI agent framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nexus-ultimate/nexus",
    packages=find_packages(exclude=["tests", "benchmark"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "python-telegram-bot>=20.0",
        "aiohttp>=3.9.0",
        "pydantic>=2.5.0",
        "pyyaml>=6.0",
        "openai>=1.10.0",
        "pillow>=10.0.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.12.0",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "nexus=nexus.cli:main",
        ],
    },
)
