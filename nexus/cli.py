"""
Command-line interface for NEXUS Ultimate
"""

import sys
import asyncio
import argparse
from pathlib import Path

from nexus import NexusAgent


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="NEXUS Ultimate - Elite Cognitive AI Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  nexus query "What is AI?"
  nexus interactive
  nexus benchmark
  nexus --config custom.yaml query "Analyze this"
        """
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='NEXUS Ultimate 1.0.0'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file',
        default=None
    )
    
    parser.add_argument(
        '--mode',
        choices=['auto', 'supervised', 'debug'],
        default='auto',
        help='Execution mode'
    )
    
    parser.add_argument(
        '--platform',
        choices=['telegram', 'web', 'api', 'cli'],
        default='cli',
        help='Target platform'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Process a query')
    query_parser.add_argument('text', type=str, help='Query text')
    query_parser.add_argument(
        '--media',
        nargs='+',
        help='Media URLs to process'
    )
    
    # Interactive command
    subparsers.add_parser('interactive', help='Start interactive mode')
    
    # Benchmark command
    subparsers.add_parser('benchmark', help='Run benchmark suite')
    
    # Test command
    subparsers.add_parser('test', help='Run tests')
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    
    # Initialize agent
    agent = NexusAgent(
        config_path=args.config,
        mode=args.mode,
        platform=args.platform
    )
    
    # Execute command
    if args.command == 'query':
        asyncio.run(handle_query(agent, args))
    elif args.command == 'interactive':
        asyncio.run(interactive_mode(agent))
    elif args.command == 'benchmark':
        run_benchmark()
    elif args.command == 'test':
        run_tests()


async def handle_query(agent, args):
    """Handle single query."""
    print(f"🧠 NEXUS Ultimate - Processing query...\n")
    
    response = await agent.process(
        query=args.text,
        media_urls=args.media or []
    )
    
    print(response.output)
    print(f"\n⏱️  Execution time: {response.metrics.get('execution_time', 0):.2f}s")


async def interactive_mode(agent):
    """Start interactive REPL mode."""
    print("🧠 NEXUS Ultimate - Interactive Mode")
    print("Type 'exit' or 'quit' to exit\n")
    
    while True:
        try:
            query = input("You: ").strip()
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("Goodbye! 👋")
                break
            
            if not query:
                continue
            
            response = await agent.process(query=query)
            print(f"\nNEXUS: {response.output}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


def run_benchmark():
    """Run benchmark suite."""
    print("🚀 Running NEXUS Benchmark Suite...\n")
    
    try:
        from benchmark.run_all import main as benchmark_main
        asyncio.run(benchmark_main())
    except ImportError:
        print("❌ Benchmark module not found. Install dev dependencies:")
        print("   pip install -r requirements-dev.txt")


def run_tests():
    """Run test suite."""
    print("🧪 Running NEXUS Test Suite...\n")
    
    import subprocess
    result = subprocess.run(
        ['pytest', 'tests/', '-v', '--cov=nexus'],
        cwd=Path(__file__).parent.parent
    )
    sys.exit(result.returncode)


if __name__ == '__main__':
    main()
