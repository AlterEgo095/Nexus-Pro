"""
Main NEXUS Agent Implementation
"""

import asyncio
from typing import Optional, Dict, Any, List
import yaml
from pathlib import Path

from nexus.cognitive import ThinkingSystem
from nexus.tools import ToolOrchestrator
from nexus.media import MediaProcessor
from nexus.output import OutputFormatter
from nexus.utils import Logger, MetricsCollector


class NexusAgent:
    """
    NEXUS Ultimate - Elite cognitive AI agent.

    Combines multi-level thinking, intelligent tool orchestration,
    universal media understanding, and optimized output formatting.
    """

    def __init__(
        self, config_path: Optional[str] = None, mode: str = "auto", platform: str = "telegram"
    ):
        """
        Initialize NEXUS agent.

        Args:
            config_path: Path to configuration file
            mode: Execution mode (auto, supervised, debug)
            platform: Target platform (telegram, web, api)
        """
        self.config = self._load_config(config_path)
        self.mode = mode
        self.platform = platform

        # Initialize core components
        self.thinking = ThinkingSystem(
            levels=self.config["cognitive"]["thinking_levels"],
            reasoning_mode=self.config["cognitive"]["reasoning_mode"],
        )

        self.tools = ToolOrchestrator(
            max_parallel=self.config["tools"]["max_parallel"],
            timeout=self.config["tools"]["timeout"],
        )

        self.media = MediaProcessor(config=self.config["media"])

        self.formatter = OutputFormatter(platform=platform, config=self.config["output"])

        self.logger = Logger(level=self.config["performance"]["log_level"])
        self.metrics = MetricsCollector(enabled=self.config["performance"]["metrics_enabled"])

    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "nexus.yaml"

        with open(config_path, "r") as f:
            return yaml.safe_load(f)

    async def process(
        self,
        query: str,
        media_urls: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> "AgentResponse":
        """
        Process user query with full NEXUS pipeline.

        Args:
            query: User query text
            media_urls: Optional list of media URLs
            context: Optional context dictionary

        Returns:
            AgentResponse with results
        """
        self.logger.info(f"Processing query: {query[:100]}...")
        start_time = asyncio.get_event_loop().time()

        try:
            # LEVEL 1: PERCEPTION
            perception = await self.thinking.perceive(
                query=query, media_urls=media_urls or [], context=context or {}
            )

            # LEVEL 2: ANALYSIS
            analysis = await self.thinking.analyze(perception)

            # LEVEL 3: STRATEGY
            strategy = await self.thinking.strategize(analysis)

            # LEVEL 4: EXECUTION

            # Process media if present
            media_results = []
            if media_urls:
                media_results = await self.media.process_batch(
                    media_urls, strategy.media_processing_plan
                )

            # Execute tool chain
            tool_results = await self.tools.execute_chain(
                strategy.tool_chain, query=query, media_results=media_results
            )

            # Synthesize results
            synthesis = await self.thinking.synthesize(
                query=query,
                perception=perception,
                analysis=analysis,
                strategy=strategy,
                tool_results=tool_results,
                media_results=media_results,
            )

            # Format output
            formatted_output = self.formatter.format(synthesis, platform=self.platform)

            # Collect metrics
            execution_time = asyncio.get_event_loop().time() - start_time
            self.metrics.record(
                {
                    "execution_time": execution_time,
                    "tools_used": len(strategy.tool_chain),
                    "media_processed": len(media_urls or []),
                    "success": True,
                }
            )

            return AgentResponse(
                output=formatted_output,
                raw_synthesis=synthesis,
                strategy=strategy,
                metrics={"execution_time": execution_time},
            )

        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            self.metrics.record({"success": False, "error": str(e)})

            # Graceful degradation
            fallback_response = self._generate_fallback_response(query, e)
            return AgentResponse(output=fallback_response, error=str(e))

    def _generate_fallback_response(self, query: str, error: Exception) -> str:
        """Generate graceful fallback response on error."""
        return self.formatter.format_error(error=error, query=query, platform=self.platform)

    # Synchronous wrapper
    def process_sync(self, query: str, **kwargs) -> "AgentResponse":
        """Synchronous version of process()."""
        return asyncio.run(self.process(query, **kwargs))


class AgentResponse:
    """Response object from NEXUS agent."""

    def __init__(
        self,
        output: str,
        raw_synthesis: Optional[Any] = None,
        strategy: Optional[Any] = None,
        metrics: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ):
        self.output = output
        self.raw_synthesis = raw_synthesis
        self.strategy = strategy
        self.metrics = metrics or {}
        self.error = error

    def __str__(self) -> str:
        return self.output

    def __repr__(self) -> str:
        return f"AgentResponse(output_length={len(self.output)}, error={self.error})"
