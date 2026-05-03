"""
Tests for Tool Orchestration
"""

import pytest
from nexus.tools import ToolOrchestrator, ToolResult


class TestToolOrchestrator:
    
    @pytest.fixture
    def orchestrator(self):
        return ToolOrchestrator(
            max_parallel=5,
            timeout=120,
            retry_attempts=1
        )
    
    @pytest.mark.asyncio
    async def test_single_tool_execution(self, orchestrator):
        """Test single tool execution."""
        tool_chain = [
            {"tool": "web_search", "params": {"query": "test"}}
        ]
        
        results = await orchestrator.execute_chain(
            tool_chain=tool_chain,
            query="test",
            media_results=[]
        )
        
        assert len(results) == 1
        assert isinstance(results[0], ToolResult)
    
    @pytest.mark.asyncio
    async def test_parallel_execution(self, orchestrator):
        """Test parallel tool execution."""
        tool_chain = [
            {"tool": "web_search", "params": {}, "parallel": True},
            {"tool": "image_search", "params": {}, "parallel": True}
        ]
        
        results = await orchestrator.execute_chain(
            tool_chain=tool_chain,
            query="test",
            media_results=[]
        )
        
        assert len(results) >= 2
    
    @pytest.mark.asyncio
    async def test_circuit_breaker(self, orchestrator):
        """Test circuit breaker functionality."""
        # Record multiple failures
        orchestrator._record_failure("test_tool")
        orchestrator._record_failure("test_tool")
        
        # Circuit should be open
        assert orchestrator._is_circuit_open("test_tool")
        
        # Reset circuit
        orchestrator._reset_circuit("test_tool")
        assert not orchestrator._is_circuit_open("test_tool")
    
    def test_fallback_mapping(self, orchestrator):
        """Test fallback tool mapping."""
        fallback = orchestrator._get_fallback_tool("crawler")
        assert fallback == "web_search"
        
        fallback = orchestrator._get_fallback_tool("understand_images")
        assert fallback == "image_search"
