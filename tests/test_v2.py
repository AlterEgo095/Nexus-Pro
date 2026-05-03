"""
Tests for NEXUS V2 components
"""

import pytest
from datetime import datetime

from nexus.decision import DecisionEngine, Context, ToolScore
from nexus.memory import MemoryLayer, EpisodicMemory, SemanticMemory, ToolMemory
from nexus.metacognition import (
    MetaCognitionLoop, Evaluator, Critic, Replanner,
    ExecutionResult, QualityMetrics, ErrorType
)
from nexus.learning import LearningSystem, FeedbackMetrics, SuggestionType
from nexus.orchestrator_v2 import NexusOrchestratorV2


class TestDecisionEngine:
    """Test Decision Engine"""
    
    def test_initialization(self):
        engine = DecisionEngine(exploration_rate=0.1)
        assert engine.exploration_rate == 0.1
        assert len(engine.weights) == 4  # 4 contexts
    
    def test_score_tool_standard(self):
        engine = DecisionEngine()
        score = engine.score_tool(
            tool_name="test_tool",
            accuracy=0.9,
            speed=0.8,
            success_rate=0.85,
            cost=0.3,
            context=Context.STANDARD
        )
        assert isinstance(score, ToolScore)
        assert score.tool_name == "test_tool"
        assert 0 <= score.final_score <= 1
    
    def test_score_tool_urgent_context(self):
        engine = DecisionEngine()
        score_urgent = engine.score_tool(
            tool_name="fast_tool",
            accuracy=0.7,
            speed=0.95,
            success_rate=0.8,
            cost=0.5,
            context=Context.URGENT
        )
        # Urgent should prioritize speed
        assert score_urgent.final_score > 0.5
    
    def test_select_tool(self):
        engine = DecisionEngine(exploration_rate=0.0)  # No exploration
        candidates = [
            ("tool_a", {"accuracy": 0.9, "speed": 0.8, "success_rate": 0.9, "cost": 0.3}),
            ("tool_b", {"accuracy": 0.7, "speed": 0.9, "success_rate": 0.8, "cost": 0.2})
        ]
        selected = engine.select_tool(candidates, Context.STANDARD)
        assert selected in ["tool_a", "tool_b"]
    
    def test_record_result(self):
        engine = DecisionEngine()
        engine.record_result("test_tool", success=True, execution_time=2.5)
        assert "test_tool" in engine.tool_history
        assert len(engine.tool_history["test_tool"]) == 1


class TestMemoryLayer:
    """Test Memory Layer"""
    
    def test_initialization(self):
        memory = MemoryLayer(max_episodic=100, max_semantic=50)
        assert memory.max_episodic == 100
        assert len(memory.episodic) == 0
    
    def test_add_episodic(self):
        memory = MemoryLayer()
        episode = EpisodicMemory(
            task_id="task_1",
            timestamp=datetime.utcnow(),
            query="test query",
            tools_used=["tool_a"],
            execution_time=1.5,
            success=True,
            result_summary="success"
        )
        memory.add_episodic(episode)
        assert len(memory.episodic) == 1
    
    def test_get_similar_tasks(self):
        memory = MemoryLayer()
        memory.add_episodic(EpisodicMemory(
            task_id="1",
            timestamp=datetime.utcnow(),
            query="analyze image",
            tools_used=["understand_images"],
            execution_time=2.0,
            success=True,
            result_summary="done"
        ))
        similar = memory.get_similar_tasks("analyze photo", limit=5)
        assert len(similar) <= 5
    
    def test_update_tool_memory(self):
        memory = MemoryLayer()
        memory.update_tool_memory(
            tool_name="test_tool",
            success=True,
            execution_time=1.2,
            cost=0.5
        )
        stats = memory.get_tool_stats("test_tool")
        assert stats is not None
        assert stats["total_calls"] == 1
        assert stats["success_rate"] == 1.0


class TestMetaCognition:
    """Test Metacognition components"""
    
    def test_evaluator(self):
        evaluator = Evaluator()
        result = ExecutionResult(
            task_id="task_1",
            success=True,
            output="result",
            execution_time=2.0,
            tools_used=["tool_a"],
            confidence=0.9
        )
        metrics = evaluator.evaluate(result, "test query")
        assert isinstance(metrics, QualityMetrics)
        assert 0 <= metrics.overall_score <= 1
    
    def test_critic(self):
        critic = Critic()
        result = ExecutionResult(
            task_id="task_1",
            success=True,
            output="result",
            execution_time=2.0,
            tools_used=["tool_a"],
            confidence=0.9
        )
        quality = QualityMetrics(
            completeness=0.9,
            accuracy=0.85,
            efficiency=0.8,
            user_satisfaction_estimate=0.85,
            overall_score=0.85
        )
        critique = critic.critique(result, quality, threshold=0.7)
        assert len(critique.strengths) > 0 or len(critique.weaknesses) > 0
    
    def test_replanner(self):
        replanner = Replanner()
        original_plan = {"tools": ["tool_a"], "context": "standard"}
        from nexus.metacognition import CritiqueReport
        critique = CritiqueReport(
            timestamp=datetime.utcnow(),
            quality_metrics=QualityMetrics(0.6, 0.6, 0.6, 0.6, 0.6),
            strengths=[],
            weaknesses=["low accuracy"],
            improvement_suggestions=["try alternative tools"],
            should_replan=True,
            confidence=0.6
        )
        new_plan = replanner.replan(original_plan, critique, ["tool_b", "tool_c"])
        assert new_plan["replanned"] is True


class TestLearningSystem:
    """Test Learning System"""
    
    def test_initialization(self):
        learning = LearningSystem()
        assert learning.feedback is not None
        assert learning.optimizer is not None
    
    def test_record_execution(self):
        learning = LearningSystem()
        learning.record_execution(
            task_id="task_1",
            execution_time=2.5,
            cost=0.3,
            success=True,
            tools_used=["tool_a"],
            context="standard"
        )
        summary = learning.feedback.get_summary()
        assert summary["total_tasks"] == 1
    
    def test_get_insights(self):
        learning = LearningSystem()
        # Record multiple tasks
        for i in range(10):
            learning.record_execution(
                task_id=f"task_{i}",
                execution_time=2.0,
                cost=0.2,
                success=True,
                tools_used=["tool_a"],
                user_satisfaction=4.0
            )
        insights = learning.get_insights()
        assert "metrics_summary" in insights
        assert "business_suggestions" in insights


class TestOrchestratorV2:
    """Test NEXUS Orchestrator V2"""
    
    def test_initialization(self):
        orch = NexusOrchestratorV2(
            exploration_rate=0.1,
            confidence_threshold=0.7
        )
        assert orch.decision_engine is not None
        assert orch.memory is not None
        assert orch.learning is not None
    
    def test_process_standard(self):
        orch = NexusOrchestratorV2()
        result = orch.process(
            query="test query",
            context=Context.STANDARD
        )
        assert "task_id" in result
        assert "selected_tools" in result
        assert result["success"] is True
    
    def test_process_urgent(self):
        orch = NexusOrchestratorV2()
        result = orch.process(
            query="urgent task",
            context=Context.URGENT
        )
        assert result["context"] == "urgent"
    
    def test_get_business_suggestions(self):
        orch = NexusOrchestratorV2()
        # Process some tasks
        for i in range(25):
            orch.process(f"query {i}", Context.STANDARD)
        
        suggestions = orch.get_business_suggestions()
        assert isinstance(suggestions, list)
    
    def test_performance_summary(self):
        orch = NexusOrchestratorV2()
        orch.process("test", Context.STANDARD)
        
        summary = orch.get_performance_summary()
        assert "decision_engine" in summary
        assert "memory" in summary
        assert "learning" in summary


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
