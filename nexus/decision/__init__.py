"""
NEXUS Decision Engine V2
========================

Intelligent tool selection with dynamic scoring, exploration, and context adaptation.

Features:
- Dynamic scoring: (accuracy×0.5) + (speed×0.2) + (success_rate×0.2) - (cost×0.1)
- Context adaptation: urgent, premium, budget modes
- Exploration rate: 10% to test alternative tools
- Learning from history
"""

import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class Context(Enum):
    """Execution context types"""
    STANDARD = "standard"
    URGENT = "urgent"
    PREMIUM = "premium"
    BUDGET = "budget"


@dataclass
class ToolScore:
    """Tool evaluation score"""
    tool_name: str
    accuracy: float  # 0-1
    speed: float  # 0-1 (1 = fastest)
    success_rate: float  # 0-1
    cost: float  # 0-1 (1 = most expensive)
    final_score: float
    confidence: float


class DecisionEngine:
    """
    Intelligent tool selection engine with adaptive scoring.
    
    Scoring formula (default):
        score = (accuracy × 0.5) + (speed × 0.2) + (success_rate × 0.2) - (cost × 0.1)
    
    Context-specific weights:
        - URGENT: speed × 0.5, accuracy × 0.3, success × 0.1, cost × 0.1
        - PREMIUM: accuracy × 0.6, success × 0.2, speed × 0.1, cost × 0.1
        - BUDGET: cost × -0.5, success × 0.3, accuracy × 0.2, speed × 0.0
    """
    
    def __init__(self, exploration_rate: float = 0.1):
        """
        Args:
            exploration_rate: Probability of testing alternative tools (0-1)
        """
        self.exploration_rate = exploration_rate
        self.tool_history: Dict[str, List[float]] = {}
        
        # Context-specific scoring weights
        self.weights = {
            Context.STANDARD: {"accuracy": 0.5, "speed": 0.2, "success_rate": 0.2, "cost": -0.1},
            Context.URGENT: {"accuracy": 0.3, "speed": 0.5, "success_rate": 0.1, "cost": -0.1},
            Context.PREMIUM: {"accuracy": 0.6, "speed": 0.1, "success_rate": 0.2, "cost": -0.1},
            Context.BUDGET: {"accuracy": 0.2, "speed": 0.0, "success_rate": 0.3, "cost": -0.5}
        }
    
    def score_tool(
        self,
        tool_name: str,
        accuracy: float,
        speed: float,
        success_rate: float,
        cost: float,
        context: Context = Context.STANDARD
    ) -> ToolScore:
        """
        Calculate tool score based on context.
        
        Args:
            tool_name: Name of the tool
            accuracy: Accuracy metric (0-1)
            speed: Speed metric (0-1, 1 = fastest)
            success_rate: Historical success rate (0-1)
            cost: Cost metric (0-1, 1 = most expensive)
            context: Execution context
            
        Returns:
            ToolScore with final score and confidence
        """
        weights = self.weights[context]
        
        final_score = (
            accuracy * weights["accuracy"] +
            speed * weights["speed"] +
            success_rate * weights["success_rate"] +
            cost * weights["cost"]
        )
        
        # Confidence based on historical data
        history = self.tool_history.get(tool_name, [])
        confidence = min(0.5 + (len(history) * 0.05), 0.95) if history else 0.5
        
        return ToolScore(
            tool_name=tool_name,
            accuracy=accuracy,
            speed=speed,
            success_rate=success_rate,
            cost=cost,
            final_score=final_score,
            confidence=confidence
        )
    
    def select_tool(
        self,
        candidates: List[Tuple[str, Dict[str, float]]],
        context: Context = Context.STANDARD
    ) -> str:
        """
        Select best tool with exploration.
        
        Args:
            candidates: List of (tool_name, metrics_dict) tuples
            context: Execution context
            
        Returns:
            Selected tool name
        """
        # Score all candidates
        scores = []
        for tool_name, metrics in candidates:
            score = self.score_tool(
                tool_name=tool_name,
                accuracy=metrics.get("accuracy", 0.7),
                speed=metrics.get("speed", 0.5),
                success_rate=metrics.get("success_rate", 0.8),
                cost=metrics.get("cost", 0.5),
                context=context
            )
            scores.append(score)
        
        # Sort by final score
        scores.sort(key=lambda x: x.final_score, reverse=True)
        
        # Exploration vs exploitation
        if random.random() < self.exploration_rate:
            # Explore: pick random tool (favor less-tested)
            weights = [1.0 / (1.0 + len(self.tool_history.get(s.tool_name, []))) for s in scores]
            selected = random.choices(scores, weights=weights, k=1)[0]
        else:
            # Exploit: pick best tool
            selected = scores[0]
        
        return selected.tool_name
    
    def record_result(self, tool_name: str, success: bool, execution_time: float):
        """
        Record tool execution result for learning.
        
        Args:
            tool_name: Name of executed tool
            success: Whether execution succeeded
            execution_time: Time taken in seconds
        """
        if tool_name not in self.tool_history:
            self.tool_history[tool_name] = []
        
        score = 1.0 if success else 0.0
        # Penalize slow executions
        if execution_time > 10.0:
            score *= 0.8
        
        self.tool_history[tool_name].append(score)
        
        # Keep last 100 results
        if len(self.tool_history[tool_name]) > 100:
            self.tool_history[tool_name] = self.tool_history[tool_name][-100:]
    
    def get_success_rate(self, tool_name: str) -> float:
        """Get historical success rate for a tool"""
        history = self.tool_history.get(tool_name, [])
        if not history:
            return 0.8  # Default optimistic
        return sum(history) / len(history)


__all__ = ["DecisionEngine", "Context", "ToolScore"]
