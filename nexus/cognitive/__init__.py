"""
Cognitive Engine - Multi-level thinking system
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class ComplexityLevel(Enum):
    """Task complexity levels."""

    TRIVIAL = "trivial"
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    EXPERT = "expert"


class ReasoningMode(Enum):
    """Available reasoning modes."""

    DIRECT = "direct"
    CHAIN_OF_THOUGHT = "chain_of_thought"
    TREE_OF_THOUGHTS = "tree_of_thoughts"
    AUTO = "auto"


@dataclass
class Perception:
    """Output from perception level."""

    request_type: str
    media_present: List[str]
    complexity: ComplexityLevel
    urgency: str
    primary_intent: str


@dataclass
class Analysis:
    """Output from analysis level."""

    real_intention: str
    implicit_context: Dict[str, Any]
    explicit_context: Dict[str, Any]
    constraints: List[str]
    hypotheses: List[str]


@dataclass
class Strategy:
    """Output from strategy level."""

    execution_path: str
    tool_chain: List[Dict[str, Any]]
    media_processing_plan: Dict[str, Any]
    contingency_plan: List[str]
    reasoning_used: ReasoningMode


class ThinkingSystem:
    """
    Multi-level cognitive thinking system.

    Implements 4-level architecture:
    1. Perception - Instant detection
    2. Analysis - Deep understanding
    3. Strategy - Optimal planning
    4. Execution - Precise action (handled by agent)
    """

    def __init__(
        self, levels: int = 4, reasoning_mode: str = "auto", certainty_threshold: float = 0.8
    ):
        self.levels = levels
        self.default_reasoning_mode = ReasoningMode(reasoning_mode)
        self.certainty_threshold = certainty_threshold

    async def perceive(
        self, query: str, media_urls: List[str], context: Dict[str, Any]
    ) -> Perception:
        """
        LEVEL 1: Instant perception.

        Detects request type, media, complexity, urgency.
        """
        # Detect complexity
        complexity = self._detect_complexity(query, media_urls)

        # Detect request type
        request_type = self._classify_request(query, media_urls)

        # Assess urgency
        urgency = self._assess_urgency(query, context)

        # Extract primary intent
        primary_intent = self._extract_intent(query)

        return Perception(
            request_type=request_type,
            media_present=media_urls,
            complexity=complexity,
            urgency=urgency,
            primary_intent=primary_intent,
        )

    async def analyze(self, perception: Perception) -> Analysis:
        """
        LEVEL 2: Deep analysis.

        Understands real intention, context, constraints.
        """
        # Distinguish real vs literal intention
        real_intention = self._infer_real_intention(perception)

        # Extract implicit context
        implicit_context = self._extract_implicit_context(perception)

        # Identify explicit context
        explicit_context = self._extract_explicit_context(perception)

        # Identify constraints
        constraints = self._identify_constraints(perception)

        # Generate hypotheses
        hypotheses = self._generate_hypotheses(perception)

        return Analysis(
            real_intention=real_intention,
            implicit_context=implicit_context,
            explicit_context=explicit_context,
            constraints=constraints,
            hypotheses=hypotheses,
        )

    async def strategize(self, analysis: Analysis) -> Strategy:
        """
        LEVEL 3: Strategic planning.

        Selects execution path, allocates tools, plans contingencies.
        """
        # Select reasoning mode
        reasoning_mode = self._select_reasoning_mode(analysis)

        # Plan execution path
        if reasoning_mode == ReasoningMode.TREE_OF_THOUGHTS:
            execution_path = await self._tree_of_thoughts(analysis)
        elif reasoning_mode == ReasoningMode.CHAIN_OF_THOUGHT:
            execution_path = await self._chain_of_thought(analysis)
        else:
            execution_path = await self._direct_reasoning(analysis)

        # Allocate tools
        tool_chain = self._allocate_tools(analysis, execution_path)

        # Plan media processing
        media_plan = self._plan_media_processing(analysis)

        # Create contingency plan
        contingency = self._create_contingency_plan(analysis, tool_chain)

        return Strategy(
            execution_path=execution_path,
            tool_chain=tool_chain,
            media_processing_plan=media_plan,
            contingency_plan=contingency,
            reasoning_used=reasoning_mode,
        )

    async def synthesize(
        self,
        query: str,
        perception: Perception,
        analysis: Analysis,
        strategy: Strategy,
        tool_results: List[Any],
        media_results: List[Any],
    ) -> Dict[str, Any]:
        """
        Synthesize all results into coherent output.
        """
        return {
            "query": query,
            "perception": perception,
            "analysis": analysis,
            "strategy": strategy,
            "tool_results": tool_results,
            "media_results": media_results,
            "synthesis": self._create_synthesis(
                query, perception, analysis, tool_results, media_results
            ),
        }

    def _detect_complexity(self, query: str, media_urls: List[str]) -> ComplexityLevel:
        """Detect task complexity."""
        # Simple heuristics (real implementation would be more sophisticated)
        word_count = len(query.split())
        has_media = len(media_urls) > 0

        if word_count <= 5 and not has_media:
            return ComplexityLevel.TRIVIAL
        elif word_count <= 15 and len(media_urls) <= 1:
            return ComplexityLevel.SIMPLE
        elif word_count <= 30 and len(media_urls) <= 3:
            return ComplexityLevel.MODERATE
        elif word_count <= 50 or len(media_urls) <= 5:
            return ComplexityLevel.COMPLEX
        else:
            return ComplexityLevel.EXPERT

    def _classify_request(self, query: str, media_urls: List[str]) -> str:
        """Classify request type."""
        query_lower = query.lower()

        if media_urls:
            if any(ext in str(media_urls) for ext in [".jpg", ".png", ".jpeg"]):
                return "image_analysis"
            elif any(ext in str(media_urls) for ext in [".mp3", ".wav"]):
                return "audio_processing"
            elif any(ext in str(media_urls) for ext in [".mp4", ".avi"]):
                return "video_processing"
            elif any(ext in str(media_urls) for ext in [".pdf", ".docx"]):
                return "document_processing"

        if any(word in query_lower for word in ["search", "find", "look up"]):
            return "information_retrieval"
        elif any(word in query_lower for word in ["analyze", "calculate", "compute"]):
            return "analysis"
        elif any(word in query_lower for word in ["create", "generate", "make"]):
            return "creation"

        return "general_query"

    def _assess_urgency(self, query: str, context: Dict[str, Any]) -> str:
        """Assess urgency level."""
        urgent_keywords = ["urgent", "asap", "quickly", "immediate", "now"]
        if any(word in query.lower() for word in urgent_keywords):
            return "urgent"
        return "normal"

    def _extract_intent(self, query: str) -> str:
        """Extract primary user intent."""
        # Simplified intent extraction
        return query.split(".")[0] if "." in query else query

    def _select_reasoning_mode(self, analysis: Analysis) -> ReasoningMode:
        """Select appropriate reasoning mode."""
        if len(analysis.hypotheses) > 3:
            return ReasoningMode.TREE_OF_THOUGHTS
        elif len(analysis.constraints) > 2:
            return ReasoningMode.CHAIN_OF_THOUGHT
        return ReasoningMode.DIRECT

    async def _tree_of_thoughts(self, analysis: Analysis) -> str:
        """Tree of Thoughts reasoning."""
        # Simplified ToT implementation
        return "tree_of_thoughts_path"

    async def _chain_of_thought(self, analysis: Analysis) -> str:
        """Chain of Thought reasoning."""
        return "chain_of_thought_path"

    async def _direct_reasoning(self, analysis: Analysis) -> str:
        """Direct reasoning."""
        return "direct_path"

    def _allocate_tools(self, analysis: Analysis, path: str) -> List[Dict[str, Any]]:
        """Allocate tools based on analysis."""
        # Simplified tool allocation
        return [{"tool": "example_tool", "params": {}}]

    def _plan_media_processing(self, analysis: Analysis) -> Dict[str, Any]:
        """Plan media processing strategy."""
        return {"strategy": "multi_pass", "exhaustive": True}

    def _create_contingency_plan(self, analysis: Analysis, tools: List[Dict]) -> List[str]:
        """Create contingency plan."""
        return ["fallback_1", "fallback_2"]

    def _infer_real_intention(self, perception: Perception) -> str:
        """Infer real user intention."""
        return perception.primary_intent

    def _extract_implicit_context(self, perception: Perception) -> Dict[str, Any]:
        """Extract implicit context."""
        return {}

    def _extract_explicit_context(self, perception: Perception) -> Dict[str, Any]:
        """Extract explicit context."""
        return {}

    def _identify_constraints(self, perception: Perception) -> List[str]:
        """Identify constraints."""
        return []

    def _generate_hypotheses(self, perception: Perception) -> List[str]:
        """Generate working hypotheses."""
        return []

    def _create_synthesis(self, query, perception, analysis, tool_results, media_results):
        """Create final synthesis."""
        return {"summary": "Results synthesized", "key_findings": [], "recommendations": []}
