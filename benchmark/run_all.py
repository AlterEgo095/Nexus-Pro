"""
Benchmark Suite for NEXUS Ultimate
"""

import asyncio
import time
from typing import List, Dict, Any
from nexus import NexusAgent


class BenchmarkCase:
    """Single benchmark test case."""
    
    def __init__(self, name: str, query: str, media_urls: List[str] = None):
        self.name = name
        self.query = query
        self.media_urls = media_urls or []
        self.result = None
        self.execution_time = 0.0
        self.success = False


class BenchmarkRunner:
    """Run benchmark suite."""
    
    def __init__(self):
        self.agent = NexusAgent(mode="auto", platform="telegram")
        self.cases = self._create_test_cases()
    
    def _create_test_cases(self) -> List[BenchmarkCase]:
        """Create 50 benchmark test cases."""
        cases = []
        
        # Simple queries (10 cases)
        simple_queries = [
            "What time is it?",
            "Hello",
            "What is 2+2?",
            "Define AI",
            "Capital of France?",
            "Who is Einstein?",
            "What is Python?",
            "Convert 10 USD to EUR",
            "Weather today",
            "Random number"
        ]
        
        for i, query in enumerate(simple_queries, 1):
            cases.append(BenchmarkCase(f"simple_{i}", query))
        
        # Search tasks (10 cases)
        search_queries = [
            "Latest news about AI",
            "Research on climate change",
            "Tesla stock analysis",
            "Best practices for Python",
            "History of the internet",
            "COVID-19 statistics",
            "Machine learning tutorials",
            "Space exploration news",
            "Quantum computing explained",
            "Cryptocurrency trends"
        ]
        
        for i, query in enumerate(search_queries, 1):
            cases.append(BenchmarkCase(f"search_{i}", query))
        
        # Media processing (10 cases)
        media_queries = [
            ("Analyze this image", ["https://example.com/img1.jpg"]),
            ("Extract text from document", ["https://example.com/doc.pdf"]),
            ("Transcribe audio", ["https://example.com/audio.mp3"]),
            ("Summarize video", ["https://example.com/video.mp4"]),
            ("Compare two images", ["https://example.com/a.jpg", "https://example.com/b.jpg"]),
            ("OCR this receipt", ["https://example.com/receipt.jpg"]),
            ("Analyze chart data", ["https://example.com/chart.png"]),
            ("Extract table from image", ["https://example.com/table.jpg"]),
            ("Process multiple docs", ["https://example.com/1.pdf", "https://example.com/2.pdf"]),
            ("Analyze screenshot", ["https://example.com/screen.png"])
        ]
        
        for i, (query, urls) in enumerate(media_queries, 1):
            cases.append(BenchmarkCase(f"media_{i}", query, urls))
        
        # Complex tasks (10 cases)
        complex_queries = [
            "Research Tesla and create financial report with charts",
            "Analyze these 5 documents and synthesize findings",
            "Compare stock performance: AAPL, GOOGL, MSFT",
            "Deep research on quantum computing applications",
            "Analyze competitor strategies and create presentation",
            "Process survey data and generate insights",
            "Investigate climate trends from multiple sources",
            "Create comprehensive market analysis report",
            "Synthesize academic papers on topic X",
            "Multi-source fact-checking investigation"
        ]
        
        for i, query in enumerate(complex_queries, 1):
            cases.append(BenchmarkCase(f"complex_{i}", query))
        
        # Edge cases (10 cases)
        edge_cases = [
            ("", []),  # Empty query
            ("A" * 1000, []),  # Very long query
            ("Query with special chars: !@#$%^&*()", []),
            ("Multiple languages: Hello مرحبا 你好", []),
            ("Code snippet: def f(x): return x**2", []),
            ("Markdown **bold** _italic_ `code`", []),
            ("URLs: https://example.com http://test.org", []),
            ("Numbers: 123 456.789 1e10", []),
            ("Ambiguous: What do you mean?", []),
            ("Contradictory: Do X but don't do X", [])
        ]
        
        for i, (query, urls) in enumerate(edge_cases, 1):
            cases.append(BenchmarkCase(f"edge_{i}", query, urls))
        
        return cases
    
    async def run_single(self, case: BenchmarkCase):
        """Run single benchmark case."""
        try:
            start = time.time()
            response = await self.agent.process(
                query=case.query,
                media_urls=case.media_urls
            )
            case.execution_time = time.time() - start
            case.result = response
            case.success = response.error is None
        except Exception as e:
            case.execution_time = time.time() - start
            case.success = False
            case.result = str(e)
    
    async def run_all(self):
        """Run all benchmark cases."""
        print("🚀 Running NEXUS Benchmark Suite (50 cases)\n")
        
        for i, case in enumerate(self.cases, 1):
            print(f"[{i}/50] Running: {case.name}...", end=" ")
            await self.run_single(case)
            status = "✅" if case.success else "❌"
            print(f"{status} ({case.execution_time:.2f}s)")
        
        self._print_summary()
    
    def _print_summary(self):
        """Print benchmark summary."""
        print("\n" + "="*60)
        print("📊 BENCHMARK RESULTS")
        print("="*60)
        
        total = len(self.cases)
        successful = sum(1 for c in self.cases if c.success)
        failed = total - successful
        
        avg_time = sum(c.execution_time for c in self.cases) / total
        min_time = min(c.execution_time for c in self.cases)
        max_time = max(c.execution_time for c in self.cases)
        
        print(f"\nTotal Cases: {total}")
        print(f"Successful: {successful} ({successful/total*100:.1f}%)")
        print(f"Failed: {failed} ({failed/total*100:.1f}%)")
        print(f"\nExecution Time:")
        print(f"  Average: {avg_time:.2f}s")
        print(f"  Min: {min_time:.2f}s")
        print(f"  Max: {max_time:.2f}s")
        
        # Category breakdown
        categories = {}
        for case in self.cases:
            cat = case.name.split('_')[0]
            if cat not in categories:
                categories[cat] = {'total': 0, 'success': 0, 'time': 0}
            categories[cat]['total'] += 1
            if case.success:
                categories[cat]['success'] += 1
            categories[cat]['time'] += case.execution_time
        
        print("\n📈 By Category:")
        for cat, stats in categories.items():
            success_rate = stats['success'] / stats['total'] * 100
            avg_cat_time = stats['time'] / stats['total']
            print(f"  {cat.capitalize()}: {success_rate:.1f}% success, {avg_cat_time:.2f}s avg")


async def main():
    runner = BenchmarkRunner()
    await runner.run_all()


if __name__ == "__main__":
    asyncio.run(main())
