# Contributing to NEXUS Ultimate

First off, thank you for considering contributing to NEXUS Ultimate! 🎉

## 🌟 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **System information** (OS, Python version, NEXUS version)
- **Logs** (if applicable)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. Include:

- **Clear use case**
- **Why this enhancement would be useful**
- **Possible implementation approach**

### Pull Requests

1. **Fork the repo** and create your branch from `main`
2. **Follow coding standards** (see below)
3. **Add tests** for new features
4. **Update documentation** if needed
5. **Ensure tests pass**: `pytest tests/`
6. **Format code**: `black nexus/`
7. **Submit PR** with clear description

## 📝 Coding Standards

### Python Style Guide

We follow PEP 8 with these specifics:

```python
# Good
def analyze_image(image_url: str, mode: str = "auto") -> dict:
    """
    Analyze image using multi-pass protocol.
    
    Args:
        image_url: URL of image to analyze
        mode: Analysis mode (auto, fast, deep)
    
    Returns:
        Analysis results dict
    """
    pass

# Bad
def analyze(url,m="auto"):
    pass
```

### Code Quality Tools

```bash
# Format code
black nexus/

# Lint
flake8 nexus/

# Type check
mypy nexus/

# Run all checks
pre-commit run --all-files
```

### Testing

```bash
# Run all tests
pytest tests/

# With coverage
pytest tests/ --cov=nexus --cov-report=html

# Specific test
pytest tests/test_cognitive.py::test_tree_of_thoughts
```

## 🏗️ Project Structure

```
nexus-ultimate/
├── nexus/
│   ├── cognitive/       # Cognitive engine
│   ├── tools/          # Tool orchestration
│   ├── media/          # Media processing
│   ├── output/         # Output formatting
│   └── utils/          # Utilities
├── tests/              # Test suite
├── benchmark/          # Benchmarks
├── config/             # Configuration
└── docs/               # Documentation
```

## 🧪 Writing Tests

### Test Structure

```python
import pytest
from nexus.cognitive import ThinkingSystem

class TestThinkingSystem:
    @pytest.fixture
    def thinking_system(self):
        return ThinkingSystem(levels=4)
    
    def test_perception_level(self, thinking_system):
        """Test perception level detection."""
        result = thinking_system.perceive(
            query="What time is it?",
            media=[]
        )
        assert result.complexity == "simple"
        assert result.urgency == "normal"
    
    def test_tree_of_thoughts(self, thinking_system):
        """Test ToT reasoning for complex problems."""
        result = thinking_system.reason(
            problem="Complex multi-step task",
            mode="tree_of_thoughts"
        )
        assert len(result.branches) >= 3
        assert result.selected_branch is not None
```

### Test Coverage

Aim for:
- **Unit tests**: ≥90% coverage
- **Integration tests**: Critical paths
- **End-to-end tests**: Main workflows

## 📚 Documentation

### Docstring Format

```python
def process_media(
    media_url: str,
    media_type: str,
    options: dict = None
) -> MediaResult:
    """
    Process media file with optimal pipeline.
    
    This function automatically selects the best processing
    pipeline based on media type and applies multi-pass
    analysis for comprehensive results.
    
    Args:
        media_url: URL or path to media file
        media_type: Type of media (image, audio, video, document)
        options: Optional processing parameters
            - exhaustive (bool): Enable exhaustive processing
            - confidence (float): Minimum confidence threshold
    
    Returns:
        MediaResult object containing:
            - content: Extracted content
            - metadata: Media metadata
            - insights: Analysis insights
    
    Raises:
        MediaProcessingError: If processing fails
        UnsupportedFormatError: If format not supported
    
    Example:
        >>> result = process_media(
        ...     "https://example.com/image.jpg",
        ...     "image",
        ...     {"exhaustive": True}
        ... )
        >>> print(result.content)
    """
    pass
```

### Adding Documentation

- Update `docs/` for major features
- Add examples to `examples/`
- Update README.md if needed

## 🔄 Development Workflow

### 1. Set Up Environment

```bash
git clone https://github.com/nexus-ultimate/nexus.git
cd nexus
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install
```

### 2. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes

- Write code
- Add tests
- Update docs
- Run checks locally

### 4. Commit Changes

```bash
git add .
git commit -m "feat: add tree of thoughts optimization"
```

**Commit message format:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `perf:` Performance improvement

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create PR on GitHub.

## 🎯 Priority Areas

We especially welcome contributions in:

1. **New tool integrations** (see `nexus/tools/`)
2. **Media processing improvements** (see `nexus/media/`)
3. **Benchmark cases** (see `benchmark/`)
4. **Documentation examples**
5. **Performance optimizations**

## 🤔 Questions?

- **Discord**: [Join our community](https://discord.gg/nexus)
- **Discussions**: [GitHub Discussions](https://github.com/nexus-ultimate/nexus/discussions)
- **Email**: nexus@example.com

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone.

### Our Standards

**Positive behavior:**
- Using welcoming language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

**Unacceptable behavior:**
- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other unprofessional conduct

### Enforcement

Violations can be reported to nexus@example.com. All complaints will be reviewed.

---

**Thank you for contributing to NEXUS Ultimate! 🚀**
