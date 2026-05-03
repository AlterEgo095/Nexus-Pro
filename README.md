# 🧠 NEXUS ULTIMATE — Cognitive AI Agent Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/nexus-ultimate/nexus)
[![Status](https://img.shields.io/badge/status-production--ready-green.svg)](https://github.com/nexus-ultimate/nexus)

> **Elite cognitive architecture for next-generation AI agents. Optimized for Telegram, mobile-first, with 30+ tool orchestration and universal media understanding.**

## 🎯 Overview

NEXUS Ultimate is an advanced AI agent framework that combines:
- **Multi-level cognitive architecture** (Perception → Analysis → Strategy → Execution)
- **Tree of Thoughts & Chain of Thought reasoning**
- **Universal media understanding** (images, documents, audio, video)
- **Intelligent tool orchestration** with automatic fallback
- **Mobile-first response optimization**
- **Proactive anticipation** and contextual suggestions

### Key Features

✨ **Cognitive Excellence**
- 4-level thinking system with meta-cognition
- Uncertainty calibration and self-correction
- Tree of Thoughts for complex problem-solving
- Adaptive reasoning based on task complexity

🔧 **Tool Mastery**
- 30+ integrated tools with smart selection
- Parallel execution for independent tasks
- Automatic fallback and error recovery
- High-performance chaining patterns

📱 **Telegram Optimization**
- Mobile-first formatting (≤2000 chars)
- Intelligent message fragmentation
- Emoji-based visual structure
- Context-aware commands

👁️ **Universal Reading**
- 100% exhaustive OCR
- Multi-pass image analysis
- Audio transcription with timestamps
- Video content extraction

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/nexus-ultimate/nexus.git
cd nexus
pip install -r requirements.txt
```

### Basic Usage

```python
from nexus import NexusAgent

# Initialize agent
agent = NexusAgent(
    mode="auto",  # or "supervised", "debug"
    platform="telegram"
)

# Process request
response = agent.process(
    query="Analyze this financial report",
    media_urls=["https://example.com/report.pdf"]
)

print(response.output)
```

### Configuration

```yaml
# config/nexus.yaml
cognitive:
  thinking_levels: 4
  reasoning_mode: "tree_of_thoughts"
  certainty_threshold: 0.8

tools:
  max_parallel: 5
  retry_attempts: 1
  timeout: 120

output:
  platform: "telegram"
  max_length: 2000
  use_emojis: true
```

## 📚 Documentation

### Architecture

```
┌─────────────────────────────────────────────┐
│         LEVEL 1: PERCEPTION                 │
│  • Request type detection                   │
│  • Media identification                     │
│  • Complexity evaluation                    │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│         LEVEL 2: ANALYSIS                   │
│  • Real intention vs literal                │
│  • Implicit/explicit context                │
│  • Constraint identification                │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│         LEVEL 3: STRATEGY                   │
│  • Execution path selection                 │
│  • Tool allocation                          │
│  • Obstacle anticipation                    │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│         LEVEL 4: EXECUTION                  │
│  • Precise action                           │
│  • Quality validation                       │
│  • Optimal formatting                       │
└─────────────────────────────────────────────┘
```

### Core Modules

#### 1. Cognitive Engine (`nexus/cognitive/`)
- `perception.py` - Input analysis and classification
- `reasoning.py` - ToT and CoT implementation
- `strategy.py` - Execution planning
- `metacognition.py` - Self-monitoring and correction

#### 2. Tool Orchestration (`nexus/tools/`)
- `selector.py` - Optimal tool selection
- `executor.py` - Parallel/sequential execution
- `fallback.py` - Error recovery
- `chains.py` - High-performance patterns

#### 3. Media Processing (`nexus/media/`)
- `vision.py` - Image understanding (OCR, analysis)
- `documents.py` - PDF, Word, Excel processing
- `audio.py` - Transcription and analysis
- `video.py` - Content extraction

#### 4. Output Formatting (`nexus/output/`)
- `telegram.py` - Telegram optimization
- `templates.py` - Response templates
- `fragmenter.py` - Smart message splitting

## 🔧 Tool Integration

### Available Tools Matrix

| Category | Tools | Use Case |
|----------|-------|----------|
| **Vision** | understand_images, image_generation, image_search | Image analysis, creation, search |
| **Search** | web_search, scholar_search, video_search | Information retrieval |
| **Execution** | Bash, Python, code sandbox | Computation, scripting |
| **Audio** | audio_transcribe, audio_generation, merge_audio | STT, TTS, audio editing |
| **Video** | video_generation, understand_video | Video creation, analysis |
| **Data** | stock_price, financial_report, product_search | Market data, analytics |
| **Geo** | maps_search, phone_call | Location, navigation |
| **Files** | aidrive_tool, file_converter | Cloud storage, conversion |

### Tool Selection Logic

```python
# Example: Automatic tool selection
def select_tools(task_type, context):
    if task_type == "image_analysis":
        return ["understand_images"]
    elif task_type == "research":
        return ["web_search", "crawler"]
    elif task_type == "computation":
        return ["Bash", "Write"]
    # ... extensive logic in nexus/tools/selector.py
```

### Chaining Patterns

```python
# High-performance chain example
async def deep_research_chain(query):
    # Step 1: Multi-source search
    results = await parallel_execute([
        web_search(query),
        scholar_search(query),
        video_search(query)
    ])
    
    # Step 2: Deep dive on top sources
    details = await sequential_execute([
        crawler(results.top_urls[0]),
        crawler(results.top_urls[1]),
        crawler(results.top_urls[2])
    ])
    
    # Step 3: Synthesize
    return synthesize(details)
```

## 📸 Media Processing

### Image Analysis Protocol

```python
# Multi-pass analysis
def analyze_image(image_url, image_type):
    # PASS 1: Identification
    content_type = identify_content(image_url)
    
    # PASS 2: Extraction
    if content_type == "document":
        text = ocr_extract(image_url, exhaustive=True)
    elif content_type == "chart":
        data = extract_data_points(image_url)
    
    # PASS 3: Semantic analysis
    insights = semantic_analysis(text or data)
    
    return {
        "content_type": content_type,
        "extracted": text or data,
        "insights": insights
    }
```

### Supported Formats

| Type | Formats | Processing |
|------|---------|------------|
| Images | JPG, PNG, WebP, GIF | OCR, object detection, analysis |
| Documents | PDF, Word, Excel, PPT | Text extraction, structure parsing |
| Audio | MP3, WAV, M4A | Transcription, speaker identification |
| Video | MP4, AVI, MOV | Transcript, scene analysis |

## 🎯 Response Optimization

### Telegram-First Design

```python
# Automatic formatting
def format_response(content, platform="telegram"):
    if platform == "telegram":
        # Mobile optimization
        content = apply_emoji_structure(content)
        content = limit_length(content, max_chars=2000)
        content = ensure_clickable_links(content)
        
        if len(content) > 2000:
            return smart_fragment(content)
    
    return content
```

### Templates

```markdown
# Standard Response Template
[Emoji] Main Result

• Key point 1
• Key point 2
• Key point 3

💡 Insight/Suggestion

🔗 [Link if applicable]
```

## 🛡️ Resilience System

### Circuit Breakers

```python
class CircuitBreaker:
    def __init__(self, max_retries=2):
        self.max_retries = max_retries
        self.attempt_count = 0
    
    def execute(self, tool, *args):
        try:
            result = tool(*args)
            self.attempt_count = 0
            return result
        except Exception as e:
            self.attempt_count += 1
            if self.attempt_count >= self.max_retries:
                return self.fallback(tool, e)
            return self.retry(tool, *args)
```

### Auto-Recovery

- **Tool Failure**: Retry (1×) → Fallback → User notification
- **Missing Data**: Complementary search
- **Ambiguity**: Proactive clarification
- **High Complexity**: Automatic decomposition

## 📊 Metrics & Monitoring

### Built-in Analytics

```python
# Track performance
metrics = {
    "response_time": agent.metrics.avg_response_time,
    "tool_success_rate": agent.metrics.tool_success_rate,
    "ocr_accuracy": agent.metrics.ocr_accuracy,
    "user_satisfaction": agent.metrics.satisfaction_score
}
```

### Logging

```python
import logging

# Configure NEXUS logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - NEXUS - %(levelname)s - %(message)s'
)
```

## 🧪 Testing

### Run Test Suite

```bash
pytest tests/ -v --cov=nexus
```

### Benchmark Suite

```bash
python benchmark/run_all.py
```

50 test cases covering:
- Simple queries
- Complex multi-tool tasks
- Media processing (all formats)
- Error handling
- Edge cases

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone repo
git clone https://github.com/nexus-ultimate/nexus.git
cd nexus

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest
```

## 📝 Roadmap

### v1.1 (Q3 2026)
- [ ] User preference learning system
- [ ] Response caching mechanism
- [ ] Advanced metrics dashboard
- [ ] Multi-language support expansion

### v1.2 (Q4 2026)
- [ ] Custom tool plugin system
- [ ] Real-time collaboration features
- [ ] Enhanced benchmark suite
- [ ] Performance optimization (20% token reduction)

### v2.0 (Q1 2027)
- [ ] Distributed execution
- [ ] Advanced reasoning modes
- [ ] Cross-platform support (WhatsApp, Slack)
- [ ] Enterprise features

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

Built with:
- OpenAI API
- Advanced reasoning patterns from research papers
- Community feedback and contributions

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/nexus-ultimate/nexus/issues)
- **Discussions**: [GitHub Discussions](https://github.com/nexus-ultimate/nexus/discussions)
- **Email**: nexus@example.com

---

**Made with 🧠 by the NEXUS Ultimate team**
