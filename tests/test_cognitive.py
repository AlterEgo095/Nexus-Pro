"""
Tests for Cognitive Engine
"""

import pytest
from nexus.cognitive import ThinkingSystem, ComplexityLevel, ReasoningMode


class TestThinkingSystem:
    
    @pytest.fixture
    def thinking_system(self):
        return ThinkingSystem(
            levels=4,
            reasoning_mode="auto",
            certainty_threshold=0.8
        )
    
    @pytest.mark.asyncio
    async def test_perception_simple_query(self, thinking_system):
        """Test perception level for simple query."""
        perception = await thinking_system.perceive(
            query="What time is it?",
            media_urls=[],
            context={}
        )
        
        assert perception.complexity == ComplexityLevel.TRIVIAL
        assert perception.media_present == []
        assert perception.urgency == "normal"
    
    @pytest.mark.asyncio
    async def test_perception_with_media(self, thinking_system):
        """Test perception with media files."""
        perception = await thinking_system.perceive(
            query="Analyze this image",
            media_urls=["https://example.com/image.jpg"],
            context={}
        )
        
        assert perception.request_type == "image_analysis"
        assert len(perception.media_present) == 1
        assert perception.complexity in [ComplexityLevel.SIMPLE, ComplexityLevel.MODERATE]
    
    @pytest.mark.asyncio
    async def test_perception_urgent_query(self, thinking_system):
        """Test urgency detection."""
        perception = await thinking_system.perceive(
            query="URGENT: Need this analyzed ASAP",
            media_urls=[],
            context={}
        )
        
        assert perception.urgency == "urgent"
    
    @pytest.mark.asyncio
    async def test_complexity_detection(self, thinking_system):
        """Test complexity level detection."""
        # Trivial
        result = thinking_system._detect_complexity("Hi", [])
        assert result == ComplexityLevel.TRIVIAL
        
        # Simple
        result = thinking_system._detect_complexity("What is Python?", [])
        assert result == ComplexityLevel.SIMPLE
        
        # Complex
        long_query = " ".join(["word"] * 60)
        result = thinking_system._detect_complexity(long_query, [])
        assert result in [ComplexityLevel.COMPLEX, ComplexityLevel.EXPERT]
    
    @pytest.mark.asyncio
    async def test_analysis_phase(self, thinking_system):
        """Test analysis phase."""
        perception = await thinking_system.perceive(
            query="Find information about Tesla",
            media_urls=[],
            context={}
        )
        
        analysis = await thinking_system.analyze(perception)
        
        assert analysis.real_intention is not None
        assert isinstance(analysis.constraints, list)
        assert isinstance(analysis.hypotheses, list)
    
    @pytest.mark.asyncio
    async def test_strategy_selection(self, thinking_system):
        """Test strategy phase and reasoning mode selection."""
        perception = await thinking_system.perceive(
            query="Complex research task with multiple steps",
            media_urls=[],
            context={}
        )
        
        analysis = await thinking_system.analyze(perception)
        strategy = await thinking_system.strategize(analysis)
        
        assert strategy.execution_path is not None
        assert isinstance(strategy.tool_chain, list)
        assert strategy.reasoning_used in [
            ReasoningMode.DIRECT,
            ReasoningMode.CHAIN_OF_THOUGHT,
            ReasoningMode.TREE_OF_THOUGHTS
        ]
    
    @pytest.mark.asyncio
    async def test_full_pipeline(self, thinking_system):
        """Test complete thinking pipeline."""
        perception = await thinking_system.perceive(
            query="Analyze this document and create a summary",
            media_urls=["https://example.com/doc.pdf"],
            context={}
        )
        
        analysis = await thinking_system.analyze(perception)
        strategy = await thinking_system.strategize(analysis)
        
        synthesis = await thinking_system.synthesize(
            query="Analyze this document and create a summary",
            perception=perception,
            analysis=analysis,
            strategy=strategy,
            tool_results=[],
            media_results=[]
        )
        
        assert 'query' in synthesis
        assert 'perception' in synthesis
        assert 'analysis' in synthesis
        assert 'strategy' in synthesis
        assert 'synthesis' in synthesis
