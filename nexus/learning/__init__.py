"""
NEXUS Learning System V2
=========================

Feedback loop and continuous improvement system.

Features:
- Metrics tracking (time, cost, success, satisfaction)
- Decision Engine updates based on feedback
- Business suggestion engine for monetization
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class SuggestionType(Enum):
    """Types of business suggestions"""
    AUTOMATION = "automation"  # Suggest workflow automation
    PREMIUM_UPGRADE = "premium_upgrade"  # Suggest premium features
    COST_OPTIMIZATION = "cost_optimization"  # Reduce costs
    PERFORMANCE_BOOST = "performance_boost"  # Improve speed/quality


@dataclass
class FeedbackMetrics:
    """Execution feedback metrics"""
    task_id: str
    timestamp: datetime
    execution_time: float
    cost: float
    success: bool
    user_satisfaction: Optional[float]  # 1-5 scale
    tools_used: List[str]
    context: str  # standard, urgent, premium, budget


@dataclass
class BusinessSuggestion:
    """Monetizable suggestion"""
    suggestion_type: SuggestionType
    title: str
    description: str
    estimated_value: float  # USD
    confidence: float
    implementation_complexity: str  # "low", "medium", "high"


class FeedbackCollector:
    """
    Collect and aggregate execution metrics.
    """
    
    def __init__(self):
        self.metrics: List[FeedbackMetrics] = []
        self.aggregates: Dict[str, Any] = {}
    
    def record(self, metrics: FeedbackMetrics):
        """
        Record execution metrics.
        
        Args:
            metrics: FeedbackMetrics instance
        """
        self.metrics.append(metrics)
        
        # Update aggregates
        if not self.aggregates:
            self.aggregates = {
                "total_tasks": 0,
                "total_time": 0.0,
                "total_cost": 0.0,
                "success_count": 0,
                "satisfaction_sum": 0.0,
                "satisfaction_count": 0,
                "tool_usage": {},
                "context_stats": {}
            }
        
        self.aggregates["total_tasks"] += 1
        self.aggregates["total_time"] += metrics.execution_time
        self.aggregates["total_cost"] += metrics.cost
        
        if metrics.success:
            self.aggregates["success_count"] += 1
        
        if metrics.user_satisfaction:
            self.aggregates["satisfaction_sum"] += metrics.user_satisfaction
            self.aggregates["satisfaction_count"] += 1
        
        for tool in metrics.tools_used:
            self.aggregates["tool_usage"][tool] = self.aggregates["tool_usage"].get(tool, 0) + 1
        
        ctx_stats = self.aggregates["context_stats"].get(metrics.context, {"count": 0, "success": 0})
        ctx_stats["count"] += 1
        if metrics.success:
            ctx_stats["success"] += 1
        self.aggregates["context_stats"][metrics.context] = ctx_stats
    
    def get_summary(self) -> Dict[str, Any]:
        """Get aggregated metrics summary"""
        if not self.aggregates or self.aggregates["total_tasks"] == 0:
            return {}
        
        total = self.aggregates["total_tasks"]
        
        return {
            "total_tasks": total,
            "avg_execution_time": self.aggregates["total_time"] / total,
            "total_cost": self.aggregates["total_cost"],
            "avg_cost_per_task": self.aggregates["total_cost"] / total,
            "success_rate": self.aggregates["success_count"] / total,
            "avg_satisfaction": (
                self.aggregates["satisfaction_sum"] / self.aggregates["satisfaction_count"]
                if self.aggregates["satisfaction_count"] > 0 else None
            ),
            "most_used_tools": sorted(
                self.aggregates["tool_usage"].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5],
            "context_performance": {
                ctx: {
                    "count": stats["count"],
                    "success_rate": stats["success"] / stats["count"]
                }
                for ctx, stats in self.aggregates["context_stats"].items()
            }
        }


class Optimizer:
    """
    Optimize decision engine based on feedback.
    """
    
    def __init__(self):
        self.optimization_history: List[Dict[str, Any]] = []
    
    def analyze_and_optimize(
        self,
        feedback: FeedbackCollector,
        current_weights: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Analyze feedback and suggest weight optimizations.
        
        Args:
            feedback: FeedbackCollector with metrics
            current_weights: Current decision engine weights
            
        Returns:
            Optimized weights
        """
        summary = feedback.get_summary()
        if not summary:
            return current_weights
        
        optimized = current_weights.copy()
        
        # If success rate is low, increase accuracy weight
        if summary["success_rate"] < 0.8:
            optimized["accuracy"] = min(optimized.get("accuracy", 0.5) + 0.05, 0.7)
        
        # If avg time is high, increase speed weight
        if summary["avg_execution_time"] > 5.0:
            optimized["speed"] = min(optimized.get("speed", 0.2) + 0.05, 0.4)
        
        # If cost is high, increase cost penalty
        if summary["avg_cost_per_task"] > 0.5:
            optimized["cost"] = max(optimized.get("cost", -0.1) - 0.05, -0.3)
        
        self.optimization_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "old_weights": current_weights,
            "new_weights": optimized,
            "trigger_metrics": {
                "success_rate": summary["success_rate"],
                "avg_time": summary["avg_execution_time"],
                "avg_cost": summary["avg_cost_per_task"]
            }
        })
        
        return optimized


class SuggestionEngine:
    """
    Generate monetizable business suggestions.
    """
    
    def __init__(self):
        self.suggestions_generated: List[BusinessSuggestion] = []
    
    def generate_suggestions(
        self,
        feedback: FeedbackCollector,
        user_context: Optional[Dict[str, Any]] = None
    ) -> List[BusinessSuggestion]:
        """
        Generate business suggestions based on usage patterns.
        
        Args:
            feedback: FeedbackCollector with metrics
            user_context: Optional user context
            
        Returns:
            List of BusinessSuggestion
        """
        suggestions = []
        summary = feedback.get_summary()
        
        if not summary or summary["total_tasks"] < 5:
            return suggestions
        
        # Automation suggestion (high-value)
        if summary["total_tasks"] > 20:
            most_used = summary["most_used_tools"][0] if summary["most_used_tools"] else None
            if most_used:
                tool_name, usage_count = most_used
                if usage_count > 10:
                    suggestions.append(BusinessSuggestion(
                        suggestion_type=SuggestionType.AUTOMATION,
                        title=f"Automate {tool_name} workflow",
                        description=f"You've used {tool_name} {usage_count} times. Set up a workflow to automate this task and save time.",
                        estimated_value=200.0,  # Estimated value
                        confidence=0.85,
                        implementation_complexity="medium"
                    ))
        
        # Premium upgrade suggestion
        if summary["avg_execution_time"] > 3.0:
            suggestions.append(BusinessSuggestion(
                suggestion_type=SuggestionType.PREMIUM_UPGRADE,
                title="Upgrade to Premium for faster execution",
                description="Premium tier offers 2x faster processing and priority tool access.",
                estimated_value=99.0,  # Monthly subscription
                confidence=0.75,
                implementation_complexity="low"
            ))
        
        # Cost optimization
        if summary["avg_cost_per_task"] > 0.3:
            suggestions.append(BusinessSuggestion(
                suggestion_type=SuggestionType.COST_OPTIMIZATION,
                title="Optimize tool usage to reduce costs",
                description="Switch to more cost-effective tools for routine tasks. Potential savings: 25%.",
                estimated_value=summary["total_cost"] * 0.25,
                confidence=0.70,
                implementation_complexity="low"
            ))
        
        # Performance boost
        if summary.get("avg_satisfaction") and summary["avg_satisfaction"] < 4.0:
            suggestions.append(BusinessSuggestion(
                suggestion_type=SuggestionType.PERFORMANCE_BOOST,
                title="Enable advanced AI features",
                description="Activate Tree-of-Thoughts reasoning and parallel execution for 40% quality improvement.",
                estimated_value=150.0,
                confidence=0.80,
                implementation_complexity="medium"
            ))
        
        self.suggestions_generated.extend(suggestions)
        return suggestions


class LearningSystem:
    """
    Complete learning system with feedback, optimization, and suggestions.
    """
    
    def __init__(self):
        self.feedback = FeedbackCollector()
        self.optimizer = Optimizer()
        self.suggestion_engine = SuggestionEngine()
    
    def record_execution(
        self,
        task_id: str,
        execution_time: float,
        cost: float,
        success: bool,
        tools_used: List[str],
        context: str = "standard",
        user_satisfaction: Optional[float] = None
    ):
        """
        Record task execution for learning.
        
        Args:
            task_id: Unique task identifier
            execution_time: Time taken in seconds
            cost: Cost in USD
            success: Whether execution succeeded
            tools_used: List of tools used
            context: Execution context
            user_satisfaction: Optional satisfaction rating (1-5)
        """
        metrics = FeedbackMetrics(
            task_id=task_id,
            timestamp=datetime.utcnow(),
            execution_time=execution_time,
            cost=cost,
            success=success,
            user_satisfaction=user_satisfaction,
            tools_used=tools_used,
            context=context
        )
        self.feedback.record(metrics)
    
    def get_insights(self) -> Dict[str, Any]:
        """Get learning insights and suggestions"""
        summary = self.feedback.get_summary()
        suggestions = self.suggestion_engine.generate_suggestions(self.feedback)
        
        return {
            "metrics_summary": summary,
            "business_suggestions": [
                {
                    "type": s.suggestion_type.value,
                    "title": s.title,
                    "description": s.description,
                    "value": f"${s.estimated_value:.2f}",
                    "confidence": f"{s.confidence*100:.1f}%"
                }
                for s in suggestions
            ],
            "total_estimated_value": sum(s.estimated_value for s in suggestions)
        }
    
    def optimize_weights(self, current_weights: Dict[str, float]) -> Dict[str, float]:
        """Get optimized decision weights"""
        return self.optimizer.analyze_and_optimize(self.feedback, current_weights)


__all__ = [
    "LearningSystem",
    "FeedbackCollector",
    "Optimizer",
    "SuggestionEngine",
    "FeedbackMetrics",
    "BusinessSuggestion",
    "SuggestionType"
]
