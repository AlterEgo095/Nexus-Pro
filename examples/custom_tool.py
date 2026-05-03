"""
Example: Custom Tool Integration

This example shows how to create and integrate a custom tool
into the NEXUS orchestration system.
"""

from typing import Dict, Any, Optional
from nexus import NexusAgent
from nexus.tools import ToolOrchestrator


class CustomWeatherTool:
    """
    Example custom tool for weather information.
    
    This demonstrates the structure needed for custom tools.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
    
    async def execute(self, location: str) -> Dict[str, Any]:
        """
        Execute weather lookup.
        
        Args:
            location: Location to get weather for
        
        Returns:
            Weather information dictionary
        """
        # Placeholder implementation
        # In real implementation, call weather API
        
        return {
            "location": location,
            "temperature": 22,
            "conditions": "Sunny",
            "humidity": 65,
            "wind_speed": 10
        }
    
    def get_tool_spec(self) -> Dict[str, Any]:
        """
        Return tool specification for orchestrator.
        
        Returns:
            Tool specification dictionary
        """
        return {
            "name": "weather_lookup",
            "description": "Get current weather for a location",
            "parameters": {
                "location": {
                    "type": "string",
                    "description": "Location name or coordinates",
                    "required": True
                }
            },
            "parallel_safe": True,  # Can run in parallel
            "timeout": 10  # Timeout in seconds
        }


class CustomToolOrchestrator(ToolOrchestrator):
    """
    Extended orchestrator with custom tool support.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_tools = {}
    
    def register_custom_tool(self, tool: Any):
        """
        Register a custom tool.
        
        Args:
            tool: Tool instance with get_tool_spec() and execute() methods
        """
        spec = tool.get_tool_spec()
        self.custom_tools[spec['name']] = tool
        print(f"✅ Registered custom tool: {spec['name']}")
    
    async def _call_tool(self, tool_spec: Dict[str, Any], previous_results=None) -> Any:
        """
        Override to support custom tools.
        """
        tool_name = tool_spec['tool']
        
        # Check if it's a custom tool
        if tool_name in self.custom_tools:
            tool = self.custom_tools[tool_name]
            params = tool_spec.get('params', {})
            return await tool.execute(**params)
        
        # Fall back to standard tools
        return await super()._call_tool(tool_spec, previous_results)


async def example_custom_tool():
    """Example: Using custom tool."""
    
    # Create custom tool
    weather_tool = CustomWeatherTool(api_key="your-api-key")
    
    # Create orchestrator with custom tool
    orchestrator = CustomToolOrchestrator(max_parallel=5, timeout=120)
    orchestrator.register_custom_tool(weather_tool)
    
    # Use in tool chain
    tool_chain = [
        {
            "tool": "weather_lookup",
            "params": {"location": "Paris"},
            "parallel": False
        }
    ]
    
    results = await orchestrator.execute_chain(
        tool_chain=tool_chain,
        query="Get weather",
        media_results=[]
    )
    
    print("Weather result:", results[0].result)


# Usage with agent
async def example_agent_with_custom_tool():
    """Example: Agent with custom tool."""
    
    # Create agent
    agent = NexusAgent(mode="auto", platform="cli")
    
    # Create and register custom tool
    weather_tool = CustomWeatherTool(api_key="your-api-key")
    
    # Extend agent's orchestrator
    custom_orchestrator = CustomToolOrchestrator(
        max_parallel=5,
        timeout=120
    )
    custom_orchestrator.register_custom_tool(weather_tool)
    
    # Replace orchestrator
    agent.tools = custom_orchestrator
    
    # Now agent can use custom tool
    response = await agent.process(
        query="What's the weather like in Paris?"
    )
    
    print(response.output)


if __name__ == "__main__":
    import asyncio
    
    print("🔧 Custom Tool Integration Example\n")
    
    # Run examples
    print("Example 1: Direct tool usage")
    asyncio.run(example_custom_tool())
    
    print("\nExample 2: Agent with custom tool")
    asyncio.run(example_agent_with_custom_tool())
