"""
NEXUS Orchestrator V2
=====================

Adaptive, learning, and business-ready orchestrator.

New Features:
- Decision Engine: Intelligent tool selection with exploration
- Memory Layer: Episodic, semantic, and tool memory
- Metacognition: Self-evaluation and replanning
- Learning System: Continuous improvement and business suggestions
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

from nexus.decision import DecisionEngine, Context
from nexus.memory import MemoryLayer, EpisodicMemory, SemanticMemory
from nexus.metacognition import MetaCognitionLoop, ExecutionResult
from nexus.learning import LearningSystem


class NexusOrchestratorV2:
    """
    NEXUS Orchestrator V2 - Adaptive AI Agent Orchestration
    
    Architecture:
        Request → Decision Engine → Memory Check → Execute → Metacognition → Learn
    
    Features:
        - Context-aware tool selection (standard, urgent, premium, budget)
        - Learning from execution history
        - Automatic replanning on low confidence
        - Business suggestion engine
    """
    
    def __init__(
        self,
        exploration_rate: float = 0.1,
        confidence_threshold: float = 0.7,
        enable_memory: bool = True,
        enable_learning: bool = True
    ):
        """
        Initialize NEXUS Orchestrator V2.
        
        Args:
            exploration_rate: Rate of exploring alternative tools (0-1)
            confidence_threshold: Minimum confidence to avoid replanning
            enable_memory: Enable memory layer
            enable_learning: Enable learning system
        """
        # Core engines
        self.decision_engine = DecisionEngine(exploration_rate=exploration_rate)
        self.metacognition = MetaCognitionLoop(confidence_threshold=confidence_threshold)
        
        # Optional systems
        self.memory = MemoryLayer() if enable_memory else None
        self.learning = LearningSystem() if enable_learning else None
        
        # Available tools (simplified - replace with actual tool registry)
        self.available_tools = [
            "web_search", "crawler", "understand_images", "image_generation",
            "audio_transcribe", "video_generation", "Bash", "code_execution",
            "stock_price", "financial_report", "maps_search"
        ]
        
        # Tool performance database (mock - replace with real metrics)
        self.tool_metrics = {
            "web_search": {"accuracy": 0.85, "speed": 0.90, "success_rate": 0.92, "cost": 0.2},
            "crawler": {"accuracy": 0.90, "speed": 0.60, "success_rate": 0.88, "cost": 0.4},
            "understand_images": {"accuracy": 0.95, "speed": 0.70, "success_rate": 0.94, "cost": 0.5},
            "image_generation": {"accuracy": 0.80, "speed": 0.50, "success_rate": 0.85, "cost": 0.8},
            "audio_transcribe": {"accuracy": 0.92, "speed": 0.75, "success_rate": 0.90, "cost": 0.3},
            "video_generation": {"accuracy": 0.75, "speed": 0.30, "success_rate": 0.80, "cost": 0.9},
            "Bash": {"accuracy": 0.88, "speed": 0.95, "success_rate": 0.85, "cost": 0.1},
            "stock_price": {"accuracy": 0.98, "speed": 0.95, "success_rate": 0.99, "cost": 0.1},
            "financial_report": {"accuracy": 0.90, "speed": 0.65, "success_rate": 0.87, "cost": 0.6},
            "maps_search": {"accuracy": 0.93, "speed": 0.85, "success_rate": 0.95, "cost": 0.2}
        }
    
    def process(
        self,
        query: str,
        context: Context = Context.STANDARD,
        user_feedback: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Process query with full V2 pipeline.
        
        Args:
            query: User query
            context: Execution context (standard, urgent, premium, budget)
            user_feedback: Optional satisfaction feedback (1-5)
            
        Returns:
            Dictionary with results and metadata
        """
        task_id = str(uuid.uuid4())
        start_time = datetime.utcnow()
        
        # Step 1: Check memory for similar tasks
        similar_tasks = []
        if self.memory:
            similar_tasks = self.memory.get_similar_tasks(query, limit=3)
        
        # Step 2: Select tools using Decision Engine
        # (Simplified: select top 2 tools based on context)
        tool_candidates = [
            (tool, metrics) for tool, metrics in self.tool_metrics.items()
        ]
        
        selected_tools = []
        for _ in range(min(2, len(tool_candidates))):
            tool = self.decision_engine.select_tool(tool_candidates, context)
            selected_tools.append(tool)
            # Remove selected from candidates to avoid duplicates
            tool_candidates = [(t, m) for t, m in tool_candidates if t != tool]
        
        # Step 3: Execute (mock execution)
        execution_time = 2.5  # Mock
        cost = sum(self.tool_metrics[t]["cost"] * 0.1 for t in selected_tools)
        success = True  # Mock
        output = f"Processed '{query}' using {', '.join(selected_tools)}"
        confidence = 0.85  # Mock
        
        result = ExecutionResult(
            task_id=task_id,
            success=success,
            output=output,
            execution_time=execution_time,
            tools_used=selected_tools,
            errors=[],
            confidence=confidence
        )
        
        # Step 4: Metacognition - Evaluate and possibly replan
        critique, new_plan = self.metacognition.process(
            result=result,
            query=query,
            original_plan={"tools": selected_tools, "context": context.value},
            available_tools=self.available_tools
        )
        
        # Step 5: Update memory
        if self.memory:
            episodic = EpisodicMemory(
                task_id=task_id,
                timestamp=start_time,
                query=query,
                tools_used=selected_tools,
                execution_time=execution_time,
                success=success,
                result_summary=output,
                context={"context": context.value, "confidence": confidence}
            )
            self.memory.add_episodic(episodic)
            
            # Update tool memory
            for tool in selected_tools:
                self.memory.update_tool_memory(
                    tool_name=tool,
                    success=success,
                    execution_time=execution_time / len(selected_tools),
                    cost=cost / len(selected_tools)
                )
        
        # Step 6: Learning - Record feedback
        if self.learning:
            self.learning.record_execution(
                task_id=task_id,
                execution_time=execution_time,
                cost=cost,
                success=success,
                tools_used=selected_tools,
                context=context.value,
                user_satisfaction=user_feedback
            )
        
        # Step 7: Record results in Decision Engine
        for tool in selected_tools:
            self.decision_engine.record_result(tool, success, execution_time)
        
        return {
            "task_id": task_id,
            "query": query,
            "context": context.value,
            "selected_tools": selected_tools,
            "execution_time": execution_time,
            "cost": cost,
            "success": success,
            "output": output,
            "confidence": confidence,
            "quality_score": critique.quality_metrics.overall_score,
            "should_replan": critique.should_replan,
            "new_plan": new_plan,
            "similar_past_tasks": len(similar_tasks),
            "critique": {
                "strengths": critique.strengths,
                "weaknesses": critique.weaknesses,
                "suggestions": critique.improvement_suggestions
            }
        }
    
    def get_business_suggestions(self) -> List[Dict[str, Any]]:
        """
        Get monetizable business suggestions.
        
        Returns:
            List of business suggestions
        """
        if not self.learning:
            return []
        
        insights = self.learning.get_insights()
        return insights.get("business_suggestions", [])
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Get performance summary across all systems.
        
        Returns:
            Dictionary with performance metrics
        """
        summary = {
            "decision_engine": {
                "exploration_rate": self.decision_engine.exploration_rate,
                "tools_tracked": len(self.decision_engine.tool_history)
            }
        }
        
        if self.memory:
            summary["memory"] = {
                "episodic_count": len(self.memory.episodic),
                "semantic_patterns": len(self.memory.semantic),
                "tools_tracked": len(self.memory.tool_memory)
            }
        
        if self.learning:
            insights = self.learning.get_insights()
            summary["learning"] = insights.get("metrics_summary", {})
            summary["business_value"] = {
                "total_estimated_value": insights.get("total_estimated_value", 0),
                "suggestions_count": len(insights.get("business_suggestions", []))
            }
        
        return summary
    
    def optimize(self):
        """
        Optimize decision weights based on learning.
        """
        if not self.learning:
            return
        
        # Get current weights for standard context
        current_weights = self.decision_engine.weights[Context.STANDARD]
        
        # Optimize
        optimized = self.learning.optimize_weights(current_weights)
        
        # Update
        self.decision_engine.weights[Context.STANDARD] = optimized
        
        print(f"✅ Optimized weights: {optimized}")


# Example usage
if __name__ == "__main__":
    # Initialize orchestrator
    orchestrator = NexusOrchestratorV2(
        exploration_rate=0.1,
        confidence_threshold=0.7,
        enable_memory=True,
        enable_learning=True
    )
    
    # Process tasks
    print("=== NEXUS Orchestrator V2 Demo ===\n")
    
    # Task 1: Standard context
    result1 = orchestrator.process(
        query="Research latest AI trends",
        context=Context.STANDARD
    )
    print(f"Task 1: {result1['selected_tools']} | Score: {result1['quality_score']:.2f}")
    
    # Task 2: Urgent context
    result2 = orchestrator.process(
        query="Quick summary of market news",
        context=Context.URGENT
    )
    print(f"Task 2: {result2['selected_tools']} | Score: {result2['quality_score']:.2f}")
    
    # Task 3: Premium context with feedback
    result3 = orchestrator.process(
        query="Create detailed financial analysis",
        context=Context.PREMIUM,
        user_feedback=4.5
    )
    print(f"Task 3: {result3['selected_tools']} | Score: {result3['quality_score']:.2f}")
    
    # Get business suggestions
    print("\n=== Business Suggestions ===")
    suggestions = orchestrator.get_business_suggestions()
    for i, sugg in enumerate(suggestions, 1):
        print(f"{i}. {sugg['title']} - Value: {sugg['value']}")
    
    # Performance summary
    print("\n=== Performance Summary ===")
    summary = orchestrator.get_performance_summary()
    print(f"Memory: {summary.get('memory', {}).get('episodic_count', 0)} tasks recorded")
    print(f"Business Value: ${summary.get('business_value', {}).get('total_estimated_value', 0):.2f}")
    
    # Optimize
    print("\n=== Optimization ===")
    orchestrator.optimize()
