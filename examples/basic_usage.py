"""
Basic usage example for NEXUS Ultimate
"""

import asyncio
from nexus import NexusAgent


async def main():
    # Initialize agent
    agent = NexusAgent(
        mode="auto",
        platform="telegram"
    )
    
    print("🧠 NEXUS Ultimate - Basic Usage Example\n")
    
    # Example 1: Simple query
    print("Example 1: Simple Query")
    print("-" * 50)
    
    response = await agent.process(
        query="What is the capital of France?"
    )
    print(response.output)
    print()
    
    # Example 2: Query with image analysis
    print("\nExample 2: Image Analysis")
    print("-" * 50)
    
    response = await agent.process(
        query="Analyze this image",
        media_urls=["https://example.com/image.jpg"]
    )
    print(response.output)
    print()
    
    # Example 3: Complex multi-step task
    print("\nExample 3: Complex Task")
    print("-" * 50)
    
    response = await agent.process(
        query="Research Tesla stock performance and create a summary report"
    )
    print(response.output)
    print()
    
    # Display metrics
    print("\n📊 Performance Metrics")
    print("-" * 50)
    stats = agent.metrics.get_stats()
    print(f"Average Response Time: {agent.metrics.avg_response_time:.2f}s")
    print(f"Tool Success Rate: {agent.metrics.tool_success_rate:.1%}")


if __name__ == "__main__":
    asyncio.run(main())
