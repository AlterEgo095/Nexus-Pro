"""
Tests for Output Formatting
"""

import pytest
from nexus.output import OutputFormatter


class TestOutputFormatter:
    
    @pytest.fixture
    def formatter(self):
        config = {
            'telegram': {
                'max_length': 2000,
                'use_emojis': True,
                'smart_fragment': True
            }
        }
        return OutputFormatter(platform="telegram", config=config)
    
    def test_telegram_formatting(self, formatter):
        """Test Telegram output formatting."""
        synthesis = {
            'query': 'test query',
            'synthesis': {
                'summary': 'Test result',
                'key_findings': ['Finding 1', 'Finding 2'],
                'recommendations': ['Rec 1', 'Rec 2']
            }
        }
        
        output = formatter.format(synthesis, platform="telegram")
        
        assert len(output) > 0
        assert 'Test result' in output
        assert '•' in output  # Bullet points
        assert '💡' in output  # Emoji present
    
    def test_length_limit(self, formatter):
        """Test length limiting."""
        long_text = "A" * 3000
        synthesis = {
            'query': 'test',
            'synthesis': {
                'summary': long_text,
                'key_findings': [],
                'recommendations': []
            }
        }
        
        output = formatter.format(synthesis, platform="telegram")
        
        # Should be fragmented
        assert len(output) <= formatter.max_length + 100  # Some buffer
    
    def test_emoji_selection(self, formatter):
        """Test emoji selection based on content."""
        synthesis_search = {'query': 'search for information'}
        emoji = formatter._select_emoji(synthesis_search)
        assert emoji == '🔍'
        
        synthesis_image = {'query': 'analyze this image'}
        emoji = formatter._select_emoji(synthesis_image)
        assert emoji == '📸'
        
        synthesis_default = {'query': 'other query'}
        emoji = formatter._select_emoji(synthesis_default)
        assert emoji == '🎯'
    
    def test_smart_fragment(self, formatter):
        """Test smart text fragmentation."""
        text = "Paragraph 1\n\n" + ("A" * 1500) + "\n\nParagraph 2\n\n" + ("B" * 1500)
        
        result = formatter._smart_fragment(text)
        
        assert len(result) <= formatter.max_length + 100
        assert "Suite" in result or len(result) < len(text)
    
    def test_error_formatting(self, formatter):
        """Test error message formatting."""
        error = Exception("Test error")
        output = formatter.format_error(error, "test query", "telegram")
        
        assert "⚠️" in output
        assert "test query" in output
