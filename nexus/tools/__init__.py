"""
Tool Orchestration System
"""

from typing import List, Dict, Any, Optional
import asyncio
from dataclasses import dataclass


@dataclass
class ToolResult:
    """Result from tool execution."""
    tool_name: str
    success: bool
    result: Any
    error: Optional[str] = None
    execution_time: float = 0.0


class ToolOrchestrator:
    """
    Intelligent tool orchestration with parallel execution,
    automatic fallback, and circuit breakers.
    """
    
    def __init__(
        self,
        max_parallel: int = 5,
        timeout: int = 120,
        retry_attempts: int = 1
    ):
        self.max_parallel = max_parallel
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.circuit_breakers = {}
    
    async def execute_chain(
        self,
        tool_chain: List[Dict[str, Any]],
        query: str,
        media_results: List[Any]
    ) -> List[ToolResult]:
        """
        Execute tool chain with optimal orchestration.
        
        Args:
            tool_chain: List of tools to execute
            query: Original query
            media_results: Results from media processing
        
        Returns:
            List of tool results
        """
        results = []
        
        # Separate parallel and sequential tasks
        parallel_tasks = []
        sequential_tasks = []
        
        for tool_spec in tool_chain:
            if tool_spec.get('parallel', False):
                parallel_tasks.append(tool_spec)
            else:
                sequential_tasks.append(tool_spec)
        
        # Execute parallel tasks
        if parallel_tasks:
            parallel_results = await self._execute_parallel(parallel_tasks)
            results.extend(parallel_results)
        
        # Execute sequential tasks
        for tool_spec in sequential_tasks:
            result = await self._execute_single(tool_spec, results)
            results.append(result)
        
        return results
    
    async def _execute_parallel(
        self,
        tools: List[Dict[str, Any]]
    ) -> List[ToolResult]:
        """Execute tools in parallel."""
        tasks = [self._execute_single(tool) for tool in tools]
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _execute_single(
        self,
        tool_spec: Dict[str, Any],
        previous_results: Optional[List[ToolResult]] = None
    ) -> ToolResult:
        """
        Execute single tool with circuit breaker and retry.
        """
        tool_name = tool_spec['tool']
        
        # Check circuit breaker
        if self._is_circuit_open(tool_name):
            return ToolResult(
                tool_name=tool_name,
                success=False,
                result=None,
                error="Circuit breaker open"
            )
        
        # Attempt execution with retry
        for attempt in range(self.retry_attempts + 1):
            try:
                result = await self._call_tool(tool_spec, previous_results)
                
                # Reset circuit breaker on success
                self._reset_circuit(tool_name)
                
                return ToolResult(
                    tool_name=tool_name,
                    success=True,
                    result=result
                )
                
            except Exception as e:
                if attempt == self.retry_attempts:
                    # Record failure in circuit breaker
                    self._record_failure(tool_name)
                    
                    # Attempt fallback
                    fallback_result = await self._attempt_fallback(
                        tool_spec, e, previous_results
                    )
                    
                    if fallback_result:
                        return fallback_result
                    
                    return ToolResult(
                        tool_name=tool_name,
                        success=False,
                        result=None,
                        error=str(e)
                    )
                
                # Wait before retry
                await asyncio.sleep(1)
    
    async def _call_tool(
        self,
        tool_spec: Dict[str, Any],
        previous_results: Optional[List[ToolResult]]
    ) -> Any:
        """
        Call the actual tool (placeholder for real implementation).
        """
        # This would call the actual tool APIs
        # For now, return mock result
        await asyncio.sleep(0.1)  # Simulate work
        return {"mock": "result"}
    
    async def _attempt_fallback(
        self,
        tool_spec: Dict[str, Any],
        error: Exception,
        previous_results: Optional[List[ToolResult]]
    ) -> Optional[ToolResult]:
        """
        Attempt fallback tool if available.
        """
        fallback_tool = self._get_fallback_tool(tool_spec['tool'])
        
        if fallback_tool:
            fallback_spec = {**tool_spec, 'tool': fallback_tool}
            return await self._execute_single(fallback_spec, previous_results)
        
        return None
    
    def _get_fallback_tool(self, tool_name: str) -> Optional[str]:
        """Get fallback tool for given tool."""
        fallback_map = {
            'crawler': 'web_search',
            'understand_images': 'image_search',
            'audio_transcribe': 'understand_video',
        }
        return fallback_map.get(tool_name)
    
    def _is_circuit_open(self, tool_name: str) -> bool:
        """Check if circuit breaker is open."""
        if tool_name not in self.circuit_breakers:
            return False
        
        breaker = self.circuit_breakers[tool_name]
        return breaker['failures'] >= 2
    
    def _record_failure(self, tool_name: str):
        """Record tool failure."""
        if tool_name not in self.circuit_breakers:
            self.circuit_breakers[tool_name] = {'failures': 0}
        
        self.circuit_breakers[tool_name]['failures'] += 1
    
    def _reset_circuit(self, tool_name: str):
        """Reset circuit breaker."""
        if tool_name in self.circuit_breakers:
            self.circuit_breakers[tool_name]['failures'] = 0
