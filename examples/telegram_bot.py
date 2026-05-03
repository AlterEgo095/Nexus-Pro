"""
Example: Telegram Bot Integration

Complete example of integrating NEXUS with Telegram bot.
"""

import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from nexus import NexusAgent


class NexusTelegramBot:
    """
    Telegram bot powered by NEXUS Ultimate.
    """
    
    def __init__(self, token: str):
        self.token = token
        self.agent = NexusAgent(mode="auto", platform="telegram")
        self.application = Application.builder().token(token).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            self.handle_message
        ))
        self.application.add_handler(MessageHandler(
            filters.PHOTO, 
            self.handle_photo
        ))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        await update.message.reply_text(
            "🧠 **NEXUS Ultimate Bot**\n\n"
            "I'm an elite cognitive AI agent. I can:\n"
            "• Answer questions\n"
            "• Analyze images\n"
            "• Process documents\n"
            "• Research topics\n"
            "• Execute code\n"
            "• And much more!\n\n"
            "Just send me a message or image!",
            parse_mode='Markdown'
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        await update.message.reply_text(
            "📚 **How to use NEXUS**\n\n"
            "**Text messages**: Just ask anything!\n"
            "• 'What is quantum computing?'\n"
            "• 'Research Tesla stock'\n"
            "• 'Calculate fibonacci(50)'\n\n"
            "**Images**: Send an image with caption\n"
            "• 'Extract text from this'\n"
            "• 'Analyze this document'\n\n"
            "**Commands**:\n"
            "/start - Start bot\n"
            "/help - Show this help\n"
            "/stats - Show statistics",
            parse_mode='Markdown'
        )
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command."""
        stats = self.agent.metrics.get_stats()
        
        await update.message.reply_text(
            f"📊 **NEXUS Statistics**\n\n"
            f"Average Response Time: {self.agent.metrics.avg_response_time:.2f}s\n"
            f"Tool Success Rate: {self.agent.metrics.tool_success_rate:.1%}\n"
            f"Total Requests: {stats.get('counters', {}).get('success_true', 0)}",
            parse_mode='Markdown'
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages."""
        user_message = update.message.text
        
        # Show typing indicator
        await update.message.chat.send_action("typing")
        
        # Process with NEXUS
        response = await self.agent.process(query=user_message)
        
        # Send response (handle long messages)
        if len(response.output) > 4000:
            # Split into chunks
            chunks = [response.output[i:i+4000] for i in range(0, len(response.output), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(response.output)
    
    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle photo messages."""
        # Get the largest photo
        photo = update.message.photo[-1]
        
        # Get file
        file = await photo.get_file()
        photo_url = file.file_path
        
        # Get caption or use default
        caption = update.message.caption or "Analyze this image"
        
        # Show typing indicator
        await update.message.chat.send_action("typing")
        
        # Process with NEXUS
        response = await self.agent.process(
            query=caption,
            media_urls=[photo_url]
        )
        
        # Send response
        await update.message.reply_text(response.output)
    
    def run(self):
        """Start the bot."""
        print("🤖 Starting NEXUS Telegram Bot...")
        print("Bot is running. Press Ctrl+C to stop.")
        self.application.run_polling()


def main():
    """Main entry point."""
    # Get token from environment
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in environment variables")
        print("\nSet it with:")
        print("  export TELEGRAM_BOT_TOKEN='your-token-here'")
        return
    
    # Create and run bot
    bot = NexusTelegramBot(token)
    bot.run()


if __name__ == "__main__":
    main()
