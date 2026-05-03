"""
NEXUS Orchestrator V2 Demo
===========================

Demonstrates the new V2 features:
- Adaptive decision engine
- Memory layer
- Metacognition loop
- Learning system with business suggestions
"""

from nexus.orchestrator_v2 import NexusOrchestratorV2
from nexus.decision import Context


def main():
    print("=" * 60)
    print("🚀 NEXUS ORCHESTRATOR V2 - DEMO")
    print("=" * 60)
    
    # Initialize orchestrator
    orchestrator = NexusOrchestratorV2(
        exploration_rate=0.1,  # 10% exploration of alternative tools
        confidence_threshold=0.7,  # Replan if confidence < 0.7
        enable_memory=True,
        enable_learning=True
    )
    
    print("\n✅ Orchestrator initialized with:")
    print("   - Exploration rate: 10%")
    print("   - Confidence threshold: 0.7")
    print("   - Memory: Enabled")
    print("   - Learning: Enabled")
    
    # Scenario 1: Standard context
    print("\n" + "=" * 60)
    print("📊 SCENARIO 1: Standard Research Task")
    print("=" * 60)
    
    result1 = orchestrator.process(
        query="Research the latest trends in artificial intelligence",
        context=Context.STANDARD
    )
    
    print(f"\n🎯 Query: {result1['query']}")
    print(f"🛠️  Selected Tools: {', '.join(result1['selected_tools'])}")
    print(f"⏱️  Execution Time: {result1['execution_time']:.2f}s")
    print(f"💰 Cost: ${result1['cost']:.3f}")
    print(f"✅ Success: {result1['success']}")
    print(f"📈 Quality Score: {result1['quality_score']:.2f}")
    print(f"🔄 Should Replan: {result1['should_replan']}")
    
    if result1['critique']['strengths']:
        print(f"\n💪 Strengths:")
        for strength in result1['critique']['strengths']:
            print(f"   • {strength}")
    
    if result1['critique']['suggestions']:
        print(f"\n💡 Suggestions:")
        for suggestion in result1['critique']['suggestions']:
            print(f"   • {suggestion}")
    
    # Scenario 2: Urgent context
    print("\n" + "=" * 60)
    print("⚡ SCENARIO 2: Urgent Market Update")
    print("=" * 60)
    
    result2 = orchestrator.process(
        query="Quick summary of today's stock market movements",
        context=Context.URGENT
    )
    
    print(f"\n🎯 Query: {result2['query']}")
    print(f"🛠️  Selected Tools: {', '.join(result2['selected_tools'])}")
    print(f"⏱️  Execution Time: {result2['execution_time']:.2f}s")
    print(f"💰 Cost: ${result2['cost']:.3f}")
    print(f"📈 Quality Score: {result2['quality_score']:.2f}")
    print("\n💡 Note: Urgent context prioritizes speed over cost")
    
    # Scenario 3: Premium context with feedback
    print("\n" + "=" * 60)
    print("💎 SCENARIO 3: Premium Financial Analysis")
    print("=" * 60)
    
    result3 = orchestrator.process(
        query="Create detailed competitive analysis of top tech companies",
        context=Context.PREMIUM,
        user_feedback=4.5  # User satisfaction: 4.5/5
    )
    
    print(f"\n🎯 Query: {result3['query']}")
    print(f"🛠️  Selected Tools: {', '.join(result3['selected_tools'])}")
    print(f"⏱️  Execution Time: {result3['execution_time']:.2f}s")
    print(f"💰 Cost: ${result3['cost']:.3f}")
    print(f"📈 Quality Score: {result3['quality_score']:.2f}")
    print(f"⭐ User Feedback: 4.5/5.0")
    print("\n💡 Note: Premium context prioritizes accuracy and quality")
    
    # Scenario 4: Budget-conscious task
    print("\n" + "=" * 60)
    print("💵 SCENARIO 4: Budget-Optimized Task")
    print("=" * 60)
    
    result4 = orchestrator.process(
        query="Summarize recent news articles",
        context=Context.BUDGET
    )
    
    print(f"\n🎯 Query: {result4['query']}")
    print(f"🛠️  Selected Tools: {', '.join(result4['selected_tools'])}")
    print(f"⏱️  Execution Time: {result4['execution_time']:.2f}s")
    print(f"💰 Cost: ${result4['cost']:.3f}")
    print(f"📈 Quality Score: {result4['quality_score']:.2f}")
    print("\n💡 Note: Budget context minimizes cost while maintaining quality")
    
    # Business Suggestions
    print("\n" + "=" * 60)
    print("💼 BUSINESS SUGGESTIONS")
    print("=" * 60)
    
    suggestions = orchestrator.get_business_suggestions()
    
    if suggestions:
        print(f"\n✨ {len(suggestions)} monetizable suggestions generated:\n")
        for i, sugg in enumerate(suggestions, 1):
            print(f"{i}. 📌 {sugg['title']}")
            print(f"   📝 {sugg['description']}")
            print(f"   💰 Estimated Value: {sugg['value']}")
            print(f"   🎯 Confidence: {sugg['confidence']}")
            print()
    else:
        print("\n⏳ Not enough data yet. Process more tasks to generate suggestions.")
    
    # Performance Summary
    print("=" * 60)
    print("📊 PERFORMANCE SUMMARY")
    print("=" * 60)
    
    summary = orchestrator.get_performance_summary()
    
    print(f"\n🧠 Decision Engine:")
    print(f"   • Exploration Rate: {summary['decision_engine']['exploration_rate']*100:.0f}%")
    print(f"   • Tools Tracked: {summary['decision_engine']['tools_tracked']}")
    
    if 'memory' in summary:
        print(f"\n💾 Memory Layer:")
        print(f"   • Episodic Memories: {summary['memory']['episodic_count']}")
        print(f"   • Semantic Patterns: {summary['memory']['semantic_patterns']}")
        print(f"   • Tools Tracked: {summary['memory']['tools_tracked']}")
    
    if 'learning' in summary:
        learning = summary['learning']
        print(f"\n📈 Learning System:")
        print(f"   • Total Tasks: {learning.get('total_tasks', 0)}")
        print(f"   • Success Rate: {learning.get('success_rate', 0)*100:.1f}%")
        print(f"   • Avg Execution Time: {learning.get('avg_execution_time', 0):.2f}s")
        print(f"   • Total Cost: ${learning.get('total_cost', 0):.3f}")
    
    if 'business_value' in summary:
        bv = summary['business_value']
        print(f"\n💰 Business Value:")
        print(f"   • Total Estimated Value: ${bv.get('total_estimated_value', 0):.2f}")
        print(f"   • Suggestions Generated: {bv.get('suggestions_count', 0)}")
    
    # Optimization
    print("\n" + "=" * 60)
    print("🔧 OPTIMIZATION")
    print("=" * 60)
    
    print("\n⚙️  Running optimization based on execution history...")
    orchestrator.optimize()
    
    print("\n✅ V2 Demo Complete!")
    print("=" * 60)
    
    # Next Steps
    print("\n📌 NEXT STEPS:")
    print("   1. Integrate with real tool implementations")
    print("   2. Connect to vector database for semantic memory")
    print("   3. Add Redis cache for episodic memory")
    print("   4. Implement persistence layer (PostgreSQL/MongoDB)")
    print("   5. Build dashboard for metrics visualization")
    print("   6. Deploy business suggestion engine")


if __name__ == "__main__":
    main()
