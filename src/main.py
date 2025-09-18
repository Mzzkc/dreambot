import os
import asyncio
from keep_alive import keep_alive
from bot import create_bot

async def main():
    """Main entry point"""
    bot = create_bot()
    keep_alive()
    await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    asyncio.run(main())