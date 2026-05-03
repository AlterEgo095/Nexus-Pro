"""
NEXUS Metacognition Layer V2
=============================

Self-evaluation, critique, and adaptive replanning system.

Features:
- Quality evaluation after execution
- Error detection and classification
- Automatic replanning when confidence < 0.7
- Learning from mistakes
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class ErrorType(Enum):
    """Error classification"""
    NETWORK = "network"  # Connectivity, timeout, API errors
    LOGIC = "logic"  # Wrong approach, invalid reasoning
    MODEL = "model"  # AI model errors (rate limits, hallucination)
    DATA = "data"  # Invalid input, missing data
    UNKNOWN = "unknown"


@dataclass
class ExecutionResult:
    """Result of task execution"""
    task_id: str
    success: bool
    output: Any
    execution_time: float
    tools_used: List[str]
    errors: List[str] = None
    confidence: float = 0.0


@dataclass
class QualityMetrics:
    """Quality evaluation metrics"""
    completeness: float  # 0-1: Did we answer everything?
    accuracy: float  # 0-1: Is the answer correct?
    efficiency: float  # 0-1: Was execution optimal?
    user_satisfaction_estimate: float  # 0-1: Predicted satisfaction
    overall_score: float  # Weighted average


@dataclass
class CritiqueReport:
    """Critique of execution"""
    timestamp: datetime
    quality_metrics: QualityMetrics
    strengths: List[str]
    weaknesses: List[str]
    improvement_suggestions: List[str]
    should_replan: bool
    confidence: float


class Evaluator:
    """
    Post-execution quality evaluation.
    """
    
    def __init__(self):
        self.evaluation_history: List[Tuple[str, QualityMetrics]] = []
    
    def evaluate(self, result: ExecutionResult, query: str) -> QualityMetrics:
        """
        Evaluate execution quality.
        
        Args:
            result: ExecutionResult to evaluate
            query: Original query
            
        Returns:
            QualityMetrics with scores
        """
        # Completeness: Did we provide output?
        completeness = 1.0 if result.output else 0.0
        if result.errors:
            completeness *= 0.5
        
        # Accuracy: Success rate and confidence
        accuracy = 1.0 if result.success else 0.3
        accuracy = (accuracy + result.confidence) / 2
        
        # Efficiency: Time and tool count
        efficiency = 1.0
        if result.execution_time > 10.0:
            efficiency *= 0.8
        if len(result.tools_used) > 5:
            efficiency *= 0.9
        
        # User satisfaction estimate (heuristic)
        user_satisfaction = (
            completeness * 0.4 +
            accuracy * 0.4 +
            efficiency * 0.2
        )
        
        # Overall score
        overall = (
            completeness * 0.3 +
            accuracy * 0.4 +
            efficiency * 0.1 +
            user_satisfaction * 0.2
        )
        
        metrics = QualityMetrics(
            completeness=completeness,
            accuracy=accuracy,
            efficiency=efficiency,
            user_satisfaction_estimate=user_satisfaction,
            overall_score=overall
        )
        
        self.evaluation_history.append((result.task_id, metrics))
        return metrics


class Critic:
    """
    Generate constructive critique and improvement suggestions.
    """
    
    def __init__(self):
        self.critique_history: List[CritiqueReport] = []
    
    def critique(
        self,
        result: ExecutionResult,
        quality: QualityMetrics,
        threshold: float = 0.7
    ) -> CritiqueReport:
        """
        Generate critique report.
        
        Args:
            result: Execution result
            quality: Quality metrics
            threshold: Confidence threshold for replanning
            
        Returns:
            CritiqueReport with analysis
        """
        strengths = []
        weaknesses = []
        suggestions = []
        
        # Analyze completeness
        if quality.completeness >= 0.9:
            strengths.append("Complete answer provided")
        elif quality.completeness < 0.5:
            weaknesses.append("Incomplete answer")
            suggestions.append("Ensure all parts of query are addressed")
        
        # Analyze accuracy
        if quality.accuracy >= 0.85:
            strengths.append("High accuracy achieved")
        elif quality.accuracy < 0.6:
            weaknesses.append("Low confidence in accuracy")
            suggestions.append("Verify results with additional sources")
        
        # Analyze efficiency
        if quality.efficiency >= 0.9:
            strengths.append("Efficient execution")
        elif quality.efficiency < 0.6:
            weaknesses.append("Suboptimal tool selection or execution")
            suggestions.append("Consider parallel execution or tool alternatives")
        
        # Analyze errors
        if result.errors:
            for error in result.errors:
                error_type = self._classify_error(error)
                weaknesses.append(f"Error encountered: {error_type.value}")
                
                if error_type == ErrorType.NETWORK:
                    suggestions.append("Implement retry with exponential backoff")
                elif error_type == ErrorType.LOGIC:
                    suggestions.append("Revise reasoning approach")
                elif error_type == ErrorType.MODEL:
                    suggestions.append("Try alternative model or tool")
        
        # Decision: should we replan?
        should_replan = quality.overall_score < threshold or len(result.errors) > 2
        
        report = CritiqueReport(
            timestamp=datetime.utcnow(),
            quality_metrics=quality,
            strengths=strengths,
            weaknesses=weaknesses,
            improvement_suggestions=suggestions,
            should_replan=should_replan,
            confidence=quality.overall_score
        )
        
        self.critique_history.append(report)
        return report
    
    def _classify_error(self, error_msg: str) -> ErrorType:
        """Classify error by message"""
        error_lower = error_msg.lower()
        
        if any(kw in error_lower for kw in ["timeout", "connection", "network", "unreachable"]):
            return ErrorType.NETWORK
        elif any(kw in error_lower for kw in ["rate limit", "quota", "model", "api key"]):
            return ErrorType.MODEL
        elif any(kw in error_lower for kw in ["invalid", "missing", "malformed", "parse"]):
            return ErrorType.DATA
        elif any(kw in error_lower for kw in ["logic", "reasoning", "incorrect"]):
            return ErrorType.LOGIC
        else:
            return ErrorType.UNKNOWN


class Replanner:
    """
    Generate alternative execution plans when needed.
    """
    
    def __init__(self):
        self.replan_history: List[Dict[str, Any]] = []
    
    def replan(
        self,
        original_plan: Dict[str, Any],
        critique: CritiqueReport,
        available_tools: List[str]
    ) -> Dict[str, Any]:
        """
        Generate alternative execution plan.
        
        Args:
            original_plan: Original execution plan
            critique: Critique report
            available_tools: Available tools
            
        Returns:
            New execution plan
        """
        new_plan = original_plan.copy()
        new_plan["replanned"] = True
        new_plan["replan_reason"] = critique.improvement_suggestions
        
        # Apply improvements based on critique
        if "parallel execution" in str(critique.improvement_suggestions):
            new_plan["parallel_execution"] = True
        
        if "alternative" in str(critique.improvement_suggestions):
            # Suggest alternative tools
            used_tools = set(original_plan.get("tools", []))
            alternatives = [t for t in available_tools if t not in used_tools]
            if alternatives:
                new_plan["alternative_tools"] = alternatives[:3]
        
        if "retry" in str(critique.improvement_suggestions):
            new_plan["retry_strategy"] = {
                "max_retries": 3,
                "backoff": "exponential"
            }
        
        # Increase confidence threshold
        new_plan["confidence_threshold"] = 0.8
        
        self.replan_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "original_plan": original_plan,
            "new_plan": new_plan,
            "critique_summary": {
                "weaknesses": critique.weaknesses,
                "suggestions": critique.improvement_suggestions
            }
        })
        
        return new_plan


class MetaCognitionLoop:
    """
    Complete metacognition loop: Evaluate → Critique → Replan (if needed).
    """
    
    def __init__(self, confidence_threshold: float = 0.7):
        """
        Args:
            confidence_threshold: Minimum confidence to avoid replanning
        """
        self.evaluator = Evaluator()
        self.critic = Critic()
        self.replanner = Replanner()
        self.confidence_threshold = confidence_threshold
    
    def process(
        self,
        result: ExecutionResult,
        query: str,
        original_plan: Dict[str, Any],
        available_tools: List[str]
    ) -> Tuple[CritiqueReport, Optional[Dict[str, Any]]]:
        """
        Run full metacognition loop.
        
        Args:
            result: Execution result to analyze
            query: Original query
            original_plan: Original execution plan
            available_tools: Available tools for replanning
            
        Returns:
            Tuple of (critique_report, new_plan or None)
        """
        # Step 1: Evaluate quality
        quality = self.evaluator.evaluate(result, query)
        
        # Step 2: Generate critique
        critique = self.critic.critique(result, quality, self.confidence_threshold)
        
        # Step 3: Replan if needed
        new_plan = None
        if critique.should_replan:
            new_plan = self.replanner.replan(original_plan, critique, available_tools)
        
        return critique, new_plan


__all__ = [
    "MetaCognitionLoop",
    "Evaluator",
    "Critic",
    "Replanner",
    "ExecutionResult",
    "QualityMetrics",
    "CritiqueReport",
    "ErrorType"
]
