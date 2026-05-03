"""
Output Formatting Module
"""

from typing import Dict, Any
import re


class OutputFormatter:
    """
    Platform-specific output formatting.
    Optimized for mobile-first (Telegram).
    """

    def __init__(self, platform: str, config: Dict[str, Any]):
        self.platform = platform
        self.config = config
        self.max_length = config.get("telegram", {}).get("max_length", 2000)
        self.use_emojis = config.get("telegram", {}).get("use_emojis", True)

    def format(self, synthesis: Dict[str, Any], platform: str = None) -> str:
        """Format synthesis into platform-optimized output."""
        platform = platform or self.platform

        if platform == "telegram":
            return self._format_telegram(synthesis)
        elif platform == "web":
            return self._format_web(synthesis)
        elif platform == "api":
            return self._format_api(synthesis)

        return str(synthesis)

    def _format_telegram(self, synthesis: Dict[str, Any]) -> str:
        """Format for Telegram (mobile-first)."""
        output_parts = []

        # Main result with emoji
        if "synthesis" in synthesis:
            main_result = synthesis["synthesis"].get("summary", "")
            emoji = self._select_emoji(synthesis)
            output_parts.append(f"{emoji} {main_result}")
            output_parts.append("")

        # Key findings as bullets
        if "synthesis" in synthesis and "key_findings" in synthesis["synthesis"]:
            findings = synthesis["synthesis"]["key_findings"]
            if findings:
                for finding in findings[:5]:  # Max 5 points
                    output_parts.append(f"• {finding}")
                output_parts.append("")

        # Insights
        if "synthesis" in synthesis and "recommendations" in synthesis["synthesis"]:
            recommendations = synthesis["synthesis"]["recommendations"]
            if recommendations:
                output_parts.append("💡 Suggestions:")
                for rec in recommendations[:3]:
                    output_parts.append(f"• {rec}")

        # Combine
        output = "\n".join(output_parts)

        # Apply length limit and fragment if needed
        if len(output) > self.max_length:
            return self._smart_fragment(output)

        return output

    def _format_web(self, synthesis: Dict[str, Any]) -> str:
        """Format for web display."""
        # Web formatting with HTML
        return f"<div class='nexus-output'>{synthesis}</div>"

    def _format_api(self, synthesis: Dict[str, Any]) -> str:
        """Format for API response (JSON)."""
        import json

        return json.dumps(synthesis, indent=2)

    def _select_emoji(self, synthesis: Dict[str, Any]) -> str:
        """Select appropriate emoji based on content."""
        query = synthesis.get("query", "").lower()

        emoji_map = {
            "search": "🔍",
            "image": "📸",
            "document": "📄",
            "calculate": "🔢",
            "analyze": "📊",
            "create": "✨",
            "video": "🎬",
            "audio": "🎵",
            "data": "📈",
            "error": "⚠️",
            "success": "✅",
        }

        for keyword, emoji in emoji_map.items():
            if keyword in query:
                return emoji

        return "🎯"  # Default

    def _smart_fragment(self, text: str) -> str:
        """
        Intelligently fragment long text.

        Splits at natural boundaries (paragraphs, sentences).
        """
        if len(text) <= self.max_length:
            return text

        # Split into paragraphs
        paragraphs = text.split("\n\n")

        fragments = []
        current_fragment = []
        current_length = 0

        for para in paragraphs:
            para_length = len(para) + 2  # +2 for \n\n

            if current_length + para_length > self.max_length:
                # Save current fragment
                if current_fragment:
                    fragments.append("\n\n".join(current_fragment))
                current_fragment = [para]
                current_length = para_length
            else:
                current_fragment.append(para)
                current_length += para_length

        # Add last fragment
        if current_fragment:
            fragments.append("\n\n".join(current_fragment))

        # Return first fragment with continuation note
        if len(fragments) > 1:
            return fragments[0] + f"\n\n📎 (Suite {len(fragments)-1}/{len(fragments)})"

        return fragments[0]

    def format_error(self, error: Exception, query: str, platform: str) -> str:
        """Format error message gracefully."""
        if platform == "telegram":
            return f"⚠️ Erreur lors du traitement\n\n💬 Requête: {query[:100]}\n\n🔧 Je peux réessayer avec une approche différente si vous le souhaitez."

        return f"Error: {error}"
