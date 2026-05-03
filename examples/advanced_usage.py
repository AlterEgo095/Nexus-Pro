"""
Advanced usage examples
"""

import asyncio
from nexus import NexusAgent


async def example_supervised_mode():
    """Example: Supervised mode with manual approval."""
    agent = NexusAgent(mode="supervised", platform="telegram")
    
    response = await agent.process(
        query="Download this dataset and analyze it",
        media_urls=["https://example.com/data.csv"]
    )
    
    print(response.output)


async def example_batch_media_processing():
    """Example: Process multiple media files."""
    agent = NexusAgent(mode="auto", platform="telegram")
    
    response = await agent.process(
        query="Analyze all these documents",
        media_urls=[
            "https://example.com/doc1.pdf",
            "https://example.com/doc2.pdf",
            "https://example.com/image1.jpg"
        ]
    )
    
    print(response.output)


async def example_custom_config():
    """Example: Custom configuration."""
    agent = NexusAgent(
        config_path="config/custom.yaml",
        mode="auto",
        platform="web"
    )
    
    response = await agent.process(
        query="Create a detailed research report on AI safety"
    )
    
    print(response.output)


async def example_with_context():
    """Example: Providing additional context."""
    agent = NexusAgent(mode="auto", platform="telegram")
    
    response = await agent.process(
        query="What's the weather like?",
        context={
            "user_location": "Paris, France",
            "user_preferences": {"units": "metric"}
        }
    )
    
    print(response.output)


if __name__ == "__main__":
    print("🧠 NEXUS Advanced Examples\n")
    
    asyncio.run(example_supervised_mode())
    print("\n" + "="*50 + "\n")
    
    asyncio.run(example_batch_media_processing())
    print("\n" + "="*50 + "\n")
    
    asyncio.run(example_with_context())
