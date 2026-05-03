# 🚀 NEXUS Ultimate — Quick Start Guide

## ⚡ Installation (60 seconds)

```bash
# 1. Clone repository
git clone https://github.com/nexus-ultimate/nexus.git
cd nexus

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure (copy and edit)
cp .env.example .env
# Edit .env with your API keys

# 4. Test installation
python -c "from nexus import NexusAgent; print('✅ Installation successful!')"
```

## 🎯 First Usage (30 seconds)

```python
from nexus import NexusAgent

# Initialize
agent = NexusAgent(mode="auto", platform="telegram")

# Simple query
response = agent.process_sync(query="What is AI?")
print(response.output)

# With image
response = agent.process_sync(
    query="Analyze this image",
    media_urls=["https://example.com/image.jpg"]
)
print(response.output)
```

## 🔧 CLI Usage

```bash
# Single query
nexus query "What is quantum computing?"

# Interactive mode
nexus interactive

# Run benchmarks
nexus benchmark

# Run tests
nexus test
```

## 🐳 Docker (Alternative)

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f nexus

# Stop
docker-compose down
```

## 📚 Key Concepts (2 minutes read)

### 1. **Cognitive Levels**
```
Perception → Analysis → Strategy → Execution
```
Agent automatically selects optimal reasoning depth.

### 2. **Modes**
- `auto` - Autonomous execution (default)
- `supervised` - Asks confirmation before actions
- `debug` - Shows reasoning process

### 3. **Platforms**
- `telegram` - Mobile-optimized (≤2000 chars)
- `web` - Full HTML formatting
- `api` - JSON responses
- `cli` - Terminal output

### 4. **Configuration**

```yaml
# config/nexus.yaml
cognitive:
  thinking_levels: 4
  reasoning_mode: "auto"

tools:
  max_parallel: 5
  timeout: 120
```

## 🎨 Common Use Cases

### Image Analysis
```python
response = agent.process_sync(
    query="Extract all text from this document",
    media_urls=["document.jpg"]
)
```

### Research & Analysis
```python
response = agent.process_sync(
    query="Research Tesla stock and create summary"
)
```

### Multi-Media Processing
```python
response = agent.process_sync(
    query="Analyze these documents",
    media_urls=["doc1.pdf", "doc2.pdf", "image.png"]
)
```

### Code Execution
```python
response = agent.process_sync(
    query="Calculate fibonacci(100) and analyze complexity"
)
```

## 🔍 Debugging

```python
# Enable debug mode
agent = NexusAgent(mode="debug")

# Check metrics
print(agent.metrics.get_stats())

# View logs
import logging
logging.getLogger("NEXUS").setLevel(logging.DEBUG)
```

## 🆘 Common Issues

### ImportError
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### API Key Issues
```bash
# Check .env file
cat .env | grep API_KEY

# Test API connection
python -c "import openai; print(openai.api_key)"
```

### Performance Issues
```yaml
# Reduce parallel execution in config/nexus.yaml
tools:
  max_parallel: 2  # Lower value
```

## 📖 Next Steps

1. **Read full docs**: [README.md](README.md)
2. **Run examples**: `python examples/basic_usage.py`
3. **Run tests**: `pytest tests/ -v`
4. **Join community**: [GitHub Discussions](https://github.com/nexus-ultimate/nexus/discussions)

## 🎓 Learning Path

1. ✅ Install & test (this guide)
2. 📘 Read [README.md](README.md) architecture section
3. 🔬 Explore [examples/](examples/)
4. 🧪 Run [benchmark/run_all.py](benchmark/run_all.py)
5. 🛠️ Customize [config/nexus.yaml](config/nexus.yaml)
6. 🚀 Build your first project

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/nexus-ultimate/nexus/issues)
- **Discussions**: [GitHub Discussions](https://github.com/nexus-ultimate/nexus/discussions)
- **Email**: nexus@example.com

---

**Total time to productivity: < 5 minutes** ⚡
