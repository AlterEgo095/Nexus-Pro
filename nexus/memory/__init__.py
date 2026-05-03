"""
NEXUS Memory Layer V2
=====================

Persistent memory system with episodic, semantic, and tool performance tracking.

Memory Types:
- Episodic: Task execution history (what, when, result)
- Semantic: Domain knowledge and patterns
- Tool Memory: Performance metrics per tool

Recommended Tech Stack:
- Vector DB: Chroma/Weaviate for semantic search
- Cache: Redis for fast episodic retrieval
- Persistence: PostgreSQL/MongoDB for logs
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class EpisodicMemory:
    """Record of a specific task execution"""
    task_id: str
    timestamp: datetime
    query: str
    tools_used: List[str]
    execution_time: float
    success: bool
    result_summary: str
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SemanticMemory:
    """Domain knowledge pattern"""
    pattern_id: str
    domain: str
    pattern_type: str  # "best_practice", "common_error", "optimization"
    description: str
    examples: List[str]
    confidence: float
    created_at: datetime
    usage_count: int = 0


@dataclass
class ToolMemory:
    """Performance history for a specific tool"""
    tool_name: str
    total_calls: int
    successful_calls: int
    avg_execution_time: float
    avg_cost: float
    error_types: Dict[str, int]  # error_type -> count
    last_used: datetime
    performance_trend: List[float]  # Recent success rates


class MemoryLayer:
    """
    Multi-type memory system for learning and adaptation.
    
    Features:
    - Episodic memory: Task execution history
    - Semantic memory: Domain patterns and knowledge
    - Tool memory: Performance tracking per tool
    - Vector search for similar past tasks (simulated)
    """
    
    def __init__(self, max_episodic: int = 1000, max_semantic: int = 500):
        """
        Args:
            max_episodic: Maximum episodic memories to retain
            max_semantic: Maximum semantic patterns to retain
        """
        self.max_episodic = max_episodic
        self.max_semantic = max_semantic
        
        # In-memory storage (replace with vector DB in production)
        self.episodic: List[EpisodicMemory] = []
        self.semantic: Dict[str, SemanticMemory] = {}
        self.tool_memory: Dict[str, ToolMemory] = {}
    
    def add_episodic(self, memory: EpisodicMemory):
        """
        Add episodic memory with automatic cleanup.
        
        Args:
            memory: EpisodicMemory instance
        """
        self.episodic.append(memory)
        
        # Keep only most recent memories
        if len(self.episodic) > self.max_episodic:
            self.episodic = self.episodic[-self.max_episodic:]
    
    def get_similar_tasks(self, query: str, limit: int = 5) -> List[EpisodicMemory]:
        """
        Find similar past tasks (simple keyword matching - use vector DB in production).
        
        Args:
            query: Current query
            limit: Maximum results
            
        Returns:
            List of similar episodic memories
        """
        # Simple keyword-based similarity (replace with vector search)
        query_words = set(query.lower().split())
        
        scored = []
        for memory in self.episodic:
            memory_words = set(memory.query.lower().split())
            overlap = len(query_words & memory_words)
            if overlap > 0:
                scored.append((overlap, memory))
        
        scored.sort(reverse=True, key=lambda x: x[0])
        return [mem for _, mem in scored[:limit]]
    
    def add_semantic(self, pattern: SemanticMemory):
        """
        Add or update semantic knowledge pattern.
        
        Args:
            pattern: SemanticMemory instance
        """
        if pattern.pattern_id in self.semantic:
            # Update existing pattern
            existing = self.semantic[pattern.pattern_id]
            existing.usage_count += 1
            existing.confidence = (existing.confidence + pattern.confidence) / 2
        else:
            self.semantic[pattern.pattern_id] = pattern
            
            # Cleanup if too many patterns
            if len(self.semantic) > self.max_semantic:
                # Remove least used patterns
                sorted_patterns = sorted(
                    self.semantic.items(),
                    key=lambda x: (x[1].usage_count, x[1].confidence)
                )
                to_remove = sorted_patterns[:len(sorted_patterns) - self.max_semantic]
                for pattern_id, _ in to_remove:
                    del self.semantic[pattern_id]
    
    def get_patterns(self, domain: Optional[str] = None) -> List[SemanticMemory]:
        """
        Retrieve semantic patterns, optionally filtered by domain.
        
        Args:
            domain: Optional domain filter
            
        Returns:
            List of semantic patterns
        """
        patterns = list(self.semantic.values())
        if domain:
            patterns = [p for p in patterns if p.domain == domain]
        
        # Sort by usage and confidence
        patterns.sort(key=lambda p: (p.usage_count, p.confidence), reverse=True)
        return patterns
    
    def update_tool_memory(
        self,
        tool_name: str,
        success: bool,
        execution_time: float,
        cost: float = 0.0,
        error_type: Optional[str] = None
    ):
        """
        Update tool performance metrics.
        
        Args:
            tool_name: Name of the tool
            success: Whether execution succeeded
            execution_time: Time taken in seconds
            cost: Cost of execution
            error_type: Type of error if failed
        """
        if tool_name not in self.tool_memory:
            self.tool_memory[tool_name] = ToolMemory(
                tool_name=tool_name,
                total_calls=0,
                successful_calls=0,
                avg_execution_time=0.0,
                avg_cost=0.0,
                error_types={},
                last_used=datetime.utcnow(),
                performance_trend=[]
            )
        
        memory = self.tool_memory[tool_name]
        memory.total_calls += 1
        if success:
            memory.successful_calls += 1
        
        # Update averages
        memory.avg_execution_time = (
            (memory.avg_execution_time * (memory.total_calls - 1) + execution_time)
            / memory.total_calls
        )
        memory.avg_cost = (
            (memory.avg_cost * (memory.total_calls - 1) + cost)
            / memory.total_calls
        )
        
        # Track errors
        if error_type:
            memory.error_types[error_type] = memory.error_types.get(error_type, 0) + 1
        
        # Update trend (last 20 executions)
        success_val = 1.0 if success else 0.0
        memory.performance_trend.append(success_val)
        if len(memory.performance_trend) > 20:
            memory.performance_trend = memory.performance_trend[-20:]
        
        memory.last_used = datetime.utcnow()
    
    def get_tool_stats(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive statistics for a tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Dictionary with tool statistics or None
        """
        if tool_name not in self.tool_memory:
            return None
        
        memory = self.tool_memory[tool_name]
        success_rate = memory.successful_calls / memory.total_calls if memory.total_calls > 0 else 0.0
        
        # Recent trend (last 10 executions)
        recent_trend = memory.performance_trend[-10:] if memory.performance_trend else []
        recent_success_rate = sum(recent_trend) / len(recent_trend) if recent_trend else 0.0
        
        return {
            "tool_name": tool_name,
            "total_calls": memory.total_calls,
            "success_rate": success_rate,
            "recent_success_rate": recent_success_rate,
            "avg_execution_time": memory.avg_execution_time,
            "avg_cost": memory.avg_cost,
            "top_errors": sorted(
                memory.error_types.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3],
            "last_used": memory.last_used.isoformat(),
            "trend": "improving" if recent_success_rate > success_rate else "declining"
        }
    
    def export_memory(self) -> Dict[str, Any]:
        """Export all memory for persistence"""
        return {
            "episodic": [
                {
                    "task_id": m.task_id,
                    "timestamp": m.timestamp.isoformat(),
                    "query": m.query,
                    "tools_used": m.tools_used,
                    "execution_time": m.execution_time,
                    "success": m.success,
                    "result_summary": m.result_summary,
                    "context": m.context
                }
                for m in self.episodic
            ],
            "semantic": {
                pid: {
                    "pattern_id": p.pattern_id,
                    "domain": p.domain,
                    "pattern_type": p.pattern_type,
                    "description": p.description,
                    "examples": p.examples,
                    "confidence": p.confidence,
                    "created_at": p.created_at.isoformat(),
                    "usage_count": p.usage_count
                }
                for pid, p in self.semantic.items()
            },
            "tool_memory": {
                name: {
                    "tool_name": t.tool_name,
                    "total_calls": t.total_calls,
                    "successful_calls": t.successful_calls,
                    "avg_execution_time": t.avg_execution_time,
                    "avg_cost": t.avg_cost,
                    "error_types": t.error_types,
                    "last_used": t.last_used.isoformat(),
                    "performance_trend": t.performance_trend
                }
                for name, t in self.tool_memory.items()
            }
        }


__all__ = ["MemoryLayer", "EpisodicMemory", "SemanticMemory", "ToolMemory"]
